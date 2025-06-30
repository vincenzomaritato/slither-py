"""
This module contains the configuration constants for the Slither game.
"""

# Screen dimensions
WIDTH = 1024
HEIGHT = 768

# Game settings
CELL_SIZE = 20
FPS = 10

# --- Synthwave Color Palette ---
BACKGROUND = (21, 2, 51)      # Dark Purple
GRID = (0, 255, 255, 50)     # Cyan with Alpha for glow
SNAKE_HEAD = (255, 0, 255)     # Bright Magenta
SNAKE_BODY = (153, 0, 204)     # Darker Magenta/Purple
SNAKE_GLOW = (255, 0, 255, 60) # Magenta with Alpha

FOOD = (255, 184, 0)         # Bright Yellow/Orange
FOOD_GLOW = (255, 184, 0, 70)  # Yellow with Alpha

TEXT = (255, 255, 255)       # White
TEXT_ACCENT = (0, 255, 255)    # Cyan
TEXT_SHADOW = (21, 2, 51, 150) # Dark transparent for readability

# Font settings
CUSTOM_FONT_PATH = "assets/fonts/pixel_font.ttf"
FONT_SIZE_S = 24
FONT_SIZE_M = 36
FONT_SIZE_L = 72

GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE