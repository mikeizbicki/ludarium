"""
NES Emulator menu item (not yet implemented).
"""

import time
import math
import pygame

DISPLAY_NAME = "NES Games"
DESCRIPTION = "Play classic NES games"


def launch(joystick=None):
    """Show 'not implemented' message with Roman flair."""
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    width, height = screen.get_size()
    pygame.mouse.set_visible(False)
    
    font = pygame.font.SysFont("serif", 48, bold=True)
    subfont = pygame.font.SysFont("serif", 32, italic=True)
    latin_font = pygame.font.SysFont("serif", 36, italic=True)
    
    # Colors
    GOLD = (212, 175, 55)
    DARK_GOLD = (153, 121, 32)
    BURGUNDY = (128, 0, 32)
    DARK_BG = (40, 35, 30)
    CREAM = (255, 253, 240)
    
    clock = pygame.time.Clock()
    start_time = time.time()
    
    running = True
    while running:
        current_time = time.time()
        elapsed = current_time - start_time
        
        # Exit after 3 seconds or on button press
        if elapsed > 3.0:
            running = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.JOYBUTTONDOWN:
                running = False
            elif event.type == pygame.KEYDOWN:
                running = False
        
        # Draw
        screen.fill(DARK_BG)
        
        # Animated border
        pulse = (math.sin(elapsed * 4) + 1) / 2
        border_color = (
            int(153 + (212 - 153) * pulse),
            int(121 + (175 - 121) * pulse),
            int(32 + (55 - 32) * pulse)
        )
        
        # Decorative columns
        col_width = 40
        col_height = height - 200
        pygame.draw.rect(screen, GOLD, (80, 100, col_width, col_height))
        pygame.draw.rect(screen, GOLD, (width - 120, 100, col_width, col_height))
        
        # Column capitals
        pygame.draw.rect(screen, DARK_GOLD, (70, 90, col_width + 20, 20))
        pygame.draw.rect(screen, DARK_GOLD, (width - 130, 90, col_width + 20, 20))
        pygame.draw.rect(screen, DARK_GOLD, (70, 100 + col_height, col_width + 20, 20))
        pygame.draw.rect(screen, DARK_GOLD, (width - 130, 100 + col_height, col_width + 20, 20))
        
        # Main border
        pygame.draw.rect(screen, border_color, (150, 50, width - 300, height - 100), 4)
        
        # Roman numeral decoration
        numeral = latin_font.render("• LUDARIUM •", True, DARK_GOLD)
        numeral_rect = numeral.get_rect(centerx=width // 2, y=80)
        screen.blit(numeral, numeral_rect)
        
        # Hourglass / waiting symbol
        cx, cy = width // 2, height // 2 - 40
        # Top triangle
        pygame.draw.polygon(screen, GOLD, [(cx - 30, cy - 40), (cx + 30, cy - 40), (cx, cy)])
        # Bottom triangle
        pygame.draw.polygon(screen, GOLD, [(cx - 30, cy + 40), (cx + 30, cy + 40), (cx, cy)])
        # Sand animation
        sand_level = int(20 * (1 - (elapsed % 1)))
        pygame.draw.rect(screen, BURGUNDY, (cx - 15, cy - 35, 30, sand_level))
        
        # Main text
        title = font.render("NONDUM PARATUM", True, GOLD)
        title_rect = title.get_rect(centerx=width // 2, y=height // 2 + 50)
        screen.blit(title, title_rect)
        
        subtitle = subfont.render("(Not Yet Ready)", True, CREAM)
        subtitle_rect = subtitle.get_rect(centerx=width // 2, y=height // 2 + 110)
        screen.blit(subtitle, subtitle_rect)
        
        desc = subfont.render("The NES emulator is being prepared...", True, (180, 170, 150))
        desc_rect = desc.get_rect(centerx=width // 2, y=height // 2 + 160)
        screen.blit(desc, desc_rect)
        
        hint = subfont.render("Press any button to return", True, (150, 140, 120))
        hint_rect = hint.get_rect(centerx=width // 2, y=height - 80)
        screen.blit(hint, hint_rect)
        
        pygame.display.flip()
        clock.tick(30)
