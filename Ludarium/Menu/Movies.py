"""
Movies menu item (not yet implemented).
"""

import time
import pygame

DISPLAY_NAME = "Movies"
DESCRIPTION = "Browse and play movie files"


def launch(joystick=None):
    """Show 'not implemented' message."""
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    width, height = screen.get_size()
    pygame.mouse.set_visible(False)
    
    font = pygame.font.SysFont("serif", 48, bold=True)
    subfont = pygame.font.SysFont("serif", 32, italic=True)
    
    # Colors
    GOLD = (212, 175, 55)
    DARK_BG = (40, 35, 30)
    CREAM = (255, 253, 240)
    
    clock = pygame.time.Clock()
    start_time = time.time()
    flash_state = True
    last_flash = start_time
    
    running = True
    while running:
        current_time = time.time()
        
        # Exit after 3 seconds or on button press
        if current_time - start_time > 3.0:
            running = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.JOYBUTTONDOWN:
                running = False
            elif event.type == pygame.KEYDOWN:
                running = False
        
        # Flash effect
        if current_time - last_flash > 0.5:
            flash_state = not flash_state
            last_flash = current_time
        
        # Draw
        screen.fill(DARK_BG)
        
        # Decorative border
        border_color = GOLD if flash_state else (153, 121, 32)
        pygame.draw.rect(screen, border_color, (50, 50, width - 100, height - 100), 4)
        
        # Construction icon (simple tools)
        cx, cy = width // 2, height // 2 - 50
        # Hammer shape
        pygame.draw.rect(screen, GOLD, (cx - 60, cy - 30, 20, 80))
        pygame.draw.rect(screen, GOLD, (cx - 80, cy - 50, 60, 25))
        # Wrench shape
        pygame.draw.rect(screen, GOLD, (cx + 40, cy - 30, 20, 80))
        pygame.draw.circle(screen, GOLD, (cx + 50, cy - 40), 20)
        pygame.draw.circle(screen, DARK_BG, (cx + 50, cy - 40), 10)
        
        # Text
        title = font.render("UNDER CONSTRUCTION", True, GOLD)
        title_rect = title.get_rect(centerx=width // 2, y=height // 2 + 60)
        screen.blit(title, title_rect)
        
        subtitle = subfont.render("This feature is not yet implemented", True, CREAM)
        subtitle_rect = subtitle.get_rect(centerx=width // 2, y=height // 2 + 130)
        screen.blit(subtitle, subtitle_rect)
        
        hint = subfont.render("Press any button to return", True, (150, 140, 120))
        hint_rect = hint.get_rect(centerx=width // 2, y=height - 100)
        screen.blit(hint, hint_rect)
        
        pygame.display.flip()
        clock.tick(30)
