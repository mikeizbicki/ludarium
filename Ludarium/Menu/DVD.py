"""
DVD Player menu item.

Plays DVDs using mplayer with gamepad control monitoring.
L+R buttons pressed simultaneously will exit playback.
"""

import subprocess
import threading
import time
import os
import signal

import pygame

DISPLAY_NAME = "DVD Player"
DESCRIPTION = "Watch DVDs from the disc drive"

# SNES Controller button mappings
BUTTON_A = 0
BUTTON_B = 1
BUTTON_X = 2
BUTTON_Y = 3
BUTTON_L = 4
BUTTON_R = 5
BUTTON_SELECT = 6
BUTTON_START = 7

HAT_UP = (0, 1)
HAT_DOWN = (0, -1)
HAT_LEFT = (-1, 0)
HAT_RIGHT = (1, 0)


class GamepadMonitor:
    """Monitor gamepad for L+R exit combo and send commands to mplayer."""
    
    def __init__(self, mplayer_process, joystick):
        self.process = mplayer_process
        self.joystick = joystick
        self.running = True
        self.thread = None
    
    def send_command(self, cmd):
        """Send a command to mplayer via stdin."""
        if self.process and self.process.poll() is None:
            try:
                self.process.stdin.write(f"{cmd}\n".encode())
                self.process.stdin.flush()
            except (BrokenPipeError, OSError):
                pass
    
    def monitor_loop(self):
        """Main monitoring loop running in background thread."""
        pygame.init()
        pygame.joystick.init()
        
        # Re-initialize joystick in this thread
        joystick = None
        if pygame.joystick.get_count() > 0:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
        
        last_hat = (0, 0)
        
        while self.running and self.process.poll() is None:
            pygame.event.pump()
            
            if joystick:
                try:
                    # Check for L+R exit combo
                    l_pressed = joystick.get_button(BUTTON_L)
                    r_pressed = joystick.get_button(BUTTON_R)
                    
                    if l_pressed and r_pressed:
                        print("L+R detected, exiting DVD player...")
                        self.send_command("quit")
                        self.running = False
                        break
                    
                    # A button - toggle pause
                    if joystick.get_button(BUTTON_A):
                        self.send_command("pause")
                        time.sleep(0.3)  # Debounce
                    
                    # B button - go back to menu (stop)
                    if joystick.get_button(BUTTON_B):
                        self.send_command("quit")
                        self.running = False
                        break
                    
                    # Start - toggle pause (alternate)
                    if joystick.get_button(BUTTON_START):
                        self.send_command("pause")
                        time.sleep(0.3)
                    
                    # Select - toggle subtitles
                    if joystick.get_button(BUTTON_SELECT):
                        self.send_command("sub_select")
                        time.sleep(0.3)
                    
                    # X button - cycle audio tracks
                    if joystick.get_button(BUTTON_X):
                        self.send_command("switch_audio")
                        time.sleep(0.3)
                    
                    # Y button - toggle fullscreen (shouldn't be needed)
                    if joystick.get_button(BUTTON_Y):
                        self.send_command("vo_fullscreen")
                        time.sleep(0.3)
                    
                    # D-pad controls
                    try:
                        hat = joystick.get_hat(0)
                        if hat != last_hat:
                            if hat == HAT_LEFT:
                                self.send_command("seek -10")
                            elif hat == HAT_RIGHT:
                                self.send_command("seek 10")
                            elif hat == HAT_UP:
                                self.send_command("seek 60")
                            elif hat == HAT_DOWN:
                                self.send_command("seek -60")
                            last_hat = hat
                    except pygame.error:
                        pass
                
                except pygame.error:
                    pass
            
            time.sleep(0.05)  # 20Hz polling
    
    def start(self):
        """Start the monitor thread."""
        self.thread = threading.Thread(target=self.monitor_loop, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Stop the monitor."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)


def find_dvd_device():
    """Find the DVD device."""
    possible_devices = [
        "/dev/dvd",
        "/dev/sr0",
        "/dev/cdrom",
        "/dev/dvdrom",
    ]
    
    for device in possible_devices:
        if os.path.exists(device):
            return device
    
    return "/dev/dvd"  # Default fallback


def launch(joystick=None):
    """Launch the DVD player."""
    dvd_device = find_dvd_device()
    
    # mplayer command for DVD playback
    # -fs: fullscreen
    # -slave: enable slave mode for commands via stdin
    # -quiet: reduce output
    # -dvd-device: specify DVD device
    cmd = [
        "mplayer",
        "-fs",
        "-slave",
        "-quiet",
        "-dvd-device", dvd_device,
        "dvd://",
    ]
    
    print(f"Launching DVD player: {' '.join(cmd)}")
    
    try:
        # Start mplayer process
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            preexec_fn=os.setsid,
        )
        
        # Start gamepad monitor
        monitor = GamepadMonitor(process, joystick)
        monitor.start()
        
        # Wait for mplayer to finish
        process.wait()
        
        # Clean up monitor
        monitor.stop()
        
    except FileNotFoundError:
        print("Error: mplayer not found. Please install mplayer.")
        show_error_message("mplayer not found")
    except Exception as e:
        print(f"Error launching DVD player: {e}")
        show_error_message(str(e))


def show_error_message(message):
    """Show an error message using pygame."""
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    width, height = screen.get_size()
    
    font = pygame.font.SysFont("serif", 36)
    title_font = pygame.font.SysFont("serif", 48, bold=True)
    
    start_time = time.time()
    
    while time.time() - start_time < 3.0:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                return
            if event.type == pygame.KEYDOWN:
                return
        
        screen.fill((60, 20, 20))
        
        title = title_font.render("DVD Error", True, (212, 175, 55))
        title_rect = title.get_rect(centerx=width // 2, y=height // 2 - 60)
        screen.blit(title, title_rect)
        
        msg = font.render(message, True, (255, 200, 200))
        msg_rect = msg.get_rect(centerx=width // 2, y=height // 2 + 20)
        screen.blit(msg, msg_rect)
        
        hint = font.render("Press any button to continue", True, (150, 150, 150))
        hint_rect = hint.get_rect(centerx=width // 2, y=height // 2 + 100)
        screen.blit(hint, hint_rect)
        
        pygame.display.flip()
        pygame.time.wait(50)
