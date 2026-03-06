#!/usr/bin/env python3
"""
Ludarium - Main menu interface.

A Roman-themed entertainment console controlled via SNES gamepad.
"""

import importlib
import os
import sys
import time
from pathlib import Path

import pygame


# SNES Controller button mappings (may vary by controller/adapter)
BUTTON_A = 0
BUTTON_B = 1
BUTTON_X = 2
BUTTON_Y = 3
BUTTON_L = 4
BUTTON_R = 5
BUTTON_SELECT = 6
BUTTON_START = 7

# D-pad is typically reported as hat 0
HAT_UP = (0, 1)
HAT_DOWN = (0, -1)
HAT_LEFT = (-1, 0)
HAT_RIGHT = (1, 0)

# Colors - Roman aesthetic palette
GOLD = (212, 175, 55)
DARK_GOLD = (153, 121, 32)
BURGUNDY = (128, 0, 32)
DARK_BURGUNDY = (80, 0, 20)
CREAM = (255, 253, 240)
DARK_CREAM = (200, 195, 170)
BRONZE = (205, 127, 50)
MARBLE_WHITE = (245, 243, 238)
MARBLE_DARK = (60, 55, 50)
SHADOW = (30, 25, 20)


def scan_menu_items():
    """Scan the Menu directory for menu item modules."""
    menu_dir = Path(__file__).parent / "Menu"
    menu_items = []
    
    if not menu_dir.exists():
        return menu_items
    
    for file in sorted(menu_dir.iterdir()):
        if file.suffix == ".py" and not file.name.startswith("_"):
            module_name = file.stem
            try:
                module = importlib.import_module(f"Ludarium.Menu.{module_name}")
                display_name = getattr(module, "DISPLAY_NAME", module_name)
                description = getattr(module, "DESCRIPTION", "")
                menu_items.append({
                    "name": module_name,
                    "display_name": display_name,
                    "description": description,
                    "module": module,
                })
            except ImportError as e:
                print(f"Warning: Could not import menu item {module_name}: {e}")
    
    return menu_items


def draw_roman_border(screen, rect, thickness=4):
    """Draw a Roman-style decorative border."""
    x, y, w, h = rect
    
    # Outer border
    pygame.draw.rect(screen, GOLD, rect, thickness)
    
    # Corner decorations (simple L-shaped flourishes)
    corner_size = 20
    
    # Top-left
    pygame.draw.line(screen, BRONZE, (x, y + corner_size), (x + corner_size, y), 3)
    # Top-right
    pygame.draw.line(screen, BRONZE, (x + w - corner_size, y), (x + w, y + corner_size), 3)
    # Bottom-left
    pygame.draw.line(screen, BRONZE, (x, y + h - corner_size), (x + corner_size, y + h), 3)
    # Bottom-right
    pygame.draw.line(screen, BRONZE, (x + w - corner_size, y + h), (x + w, y + h - corner_size), 3)


def draw_laurel_decoration(screen, center_x, y, size=30):
    """Draw a simple laurel wreath decoration."""
    # Left branch
    for i in range(5):
        angle_offset = i * 15
        leaf_x = center_x - 50 - i * 8
        leaf_y = y - 10 + abs(i - 2) * 5
        pygame.draw.ellipse(screen, DARK_GOLD, (leaf_x, leaf_y, 15, 8))
    
    # Right branch (mirrored)
    for i in range(5):
        angle_offset = i * 15
        leaf_x = center_x + 35 + i * 8
        leaf_y = y - 10 + abs(i - 2) * 5
        pygame.draw.ellipse(screen, DARK_GOLD, (leaf_x, leaf_y, 15, 8))


class LudariumMenu:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        
        # Set up fullscreen display
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_width, self.screen_height = self.screen.get_size()
        pygame.display.set_caption("LUDARIUM")
        pygame.mouse.set_visible(False)
        
        # Initialize joystick
        self.joystick = None
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print(f"Controller detected: {self.joystick.get_name()}")
        else:
            print("Warning: No controller detected!")
        
        # Fonts - using system fonts with Roman-style choices
        self.title_font = pygame.font.SysFont("serif", 72, bold=True)
        self.menu_font = pygame.font.SysFont("serif", 48)
        self.desc_font = pygame.font.SysFont("serif", 28, italic=True)
        self.hint_font = pygame.font.SysFont("serif", 24)
        
        # Menu state
        self.menu_items = scan_menu_items()
        self.selected_index = 0
        self.running = True
        
        # Animation state
        self.selection_pulse = 0
        self.last_input_time = 0
        self.input_cooldown = 0.2  # seconds
        
        # Clock for frame limiting
        self.clock = pygame.time.Clock()

    def handle_input(self):
        """Handle gamepad and keyboard input."""
        current_time = time.time()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Keyboard fallback for testing
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_UP:
                    self.navigate(-1)
                elif event.key == pygame.K_DOWN:
                    self.navigate(1)
                elif event.key == pygame.K_RETURN:
                    self.select_item()
            
            # Joystick button press
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == BUTTON_A:
                    self.select_item()
                elif event.button == BUTTON_START:
                    self.select_item()
            
            # D-pad (hat) movement
            elif event.type == pygame.JOYHATMOTION:
                if current_time - self.last_input_time > self.input_cooldown:
                    if event.value == HAT_UP:
                        self.navigate(-1)
                        self.last_input_time = current_time
                    elif event.value == HAT_DOWN:
                        self.navigate(1)
                        self.last_input_time = current_time
        
        # Check for L+R to exit (emergency exit)
        if self.joystick:
            try:
                l_pressed = self.joystick.get_button(BUTTON_L)
                r_pressed = self.joystick.get_button(BUTTON_R)
                if l_pressed and r_pressed:
                    self.running = False
            except pygame.error:
                pass

    def navigate(self, direction):
        """Navigate the menu up or down."""
        if self.menu_items:
            self.selected_index = (self.selected_index + direction) % len(self.menu_items)

    def select_item(self):
        """Select and launch the current menu item."""
        if not self.menu_items:
            return
        
        item = self.menu_items[self.selected_index]
        module = item["module"]
        
        if hasattr(module, "launch"):
            # Minimize pygame before launching external program
            pygame.display.iconify()
            try:
                module.launch(self.joystick)
            except Exception as e:
                print(f"Error launching {item['name']}: {e}")
            finally:
                # Restore display after returning
                self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                pygame.mouse.set_visible(False)

    def draw(self):
        """Draw the menu interface."""
        # Background
        self.screen.fill(MARBLE_DARK)
        
        # Draw decorative background pattern
        for i in range(0, self.screen_width, 100):
            pygame.draw.line(self.screen, (70, 65, 60), (i, 0), (i, self.screen_height), 1)
        for i in range(0, self.screen_height, 100):
            pygame.draw.line(self.screen, (70, 65, 60), (0, i), (self.screen_width, i), 1)
        
        # Title area
        title_text = self.title_font.render("LUDARIUM", True, GOLD)
        title_rect = title_text.get_rect(centerx=self.screen_width // 2, y=50)
        
        # Title shadow
        shadow_text = self.title_font.render("LUDARIUM", True, SHADOW)
        self.screen.blit(shadow_text, (title_rect.x + 4, title_rect.y + 4))
        self.screen.blit(title_text, title_rect)
        
        # Laurel decoration under title
        draw_laurel_decoration(self.screen, self.screen_width // 2, title_rect.bottom + 20)
        
        # Subtitle
        subtitle = self.desc_font.render("Entertainment Console", True, DARK_CREAM)
        subtitle_rect = subtitle.get_rect(centerx=self.screen_width // 2, y=title_rect.bottom + 40)
        self.screen.blit(subtitle, subtitle_rect)
        
        # Menu area
        menu_start_y = 220
        menu_item_height = 80
        menu_width = 500
        menu_x = (self.screen_width - menu_width) // 2
        
        # Draw menu border
        menu_border_rect = (
            menu_x - 30,
            menu_start_y - 20,
            menu_width + 60,
            len(self.menu_items) * menu_item_height + 40
        )
        pygame.draw.rect(self.screen, (50, 45, 40), menu_border_rect)
        draw_roman_border(self.screen, menu_border_rect)
        
        # Draw menu items
        self.selection_pulse = (self.selection_pulse + 0.1) % (2 * 3.14159)
        pulse_offset = int(3 * abs(pygame.math.Vector2(1, 0).rotate(self.selection_pulse * 57.3).x))
        
        for i, item in enumerate(self.menu_items):
            y = menu_start_y + i * menu_item_height
            
            if i == self.selected_index:
                # Selected item background with pulse effect
                select_rect = (menu_x - 10 - pulse_offset, y - 5, menu_width + 20 + pulse_offset * 2, 60)
                pygame.draw.rect(self.screen, BURGUNDY, select_rect)
                pygame.draw.rect(self.screen, GOLD, select_rect, 3)
                
                # Selected item text
                text = self.menu_font.render(item["display_name"], True, GOLD)
                
                # Selection indicator
                indicator = self.menu_font.render("►", True, GOLD)
                self.screen.blit(indicator, (menu_x - 50, y))
            else:
                text = self.menu_font.render(item["display_name"], True, CREAM)
            
            text_rect = text.get_rect(centerx=self.screen_width // 2, y=y)
            self.screen.blit(text, text_rect)
        
        # Description of selected item
        if self.menu_items:
            desc = self.menu_items[self.selected_index]["description"]
            if desc:
                desc_text = self.desc_font.render(desc, True, DARK_CREAM)
                desc_rect = desc_text.get_rect(centerx=self.screen_width // 2, y=menu_start_y + len(self.menu_items) * menu_item_height + 40)
                self.screen.blit(desc_text, desc_rect)
        
        # Control hints at bottom
        hint_y = self.screen_height - 60
        hints = "A/START: Select   |   D-PAD: Navigate   |   L+R: Exit"
        hint_text = self.hint_font.render(hints, True, DARK_GOLD)
        hint_rect = hint_text.get_rect(centerx=self.screen_width // 2, y=hint_y)
        self.screen.blit(hint_text, hint_rect)
        
        pygame.display.flip()

    def run(self):
        """Main loop."""
        while self.running:
            self.handle_input()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()


def main():
    """Entry point."""
    menu = LudariumMenu()
    menu.run()


if __name__ == "__main__":
    main()
