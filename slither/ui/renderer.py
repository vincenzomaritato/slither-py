"""
This module contains the Renderer class for the Slither game.
"""

from typing import TYPE_CHECKING
import pygame
import math
from pathlib import Path
from slither import config
from slither.core.gamestate import GameState

if TYPE_CHECKING:
    from slither.core.board import Board
    from slither.core.snake import Snake
    from slither.core.food import Food

class Renderer:
    """Handles all rendering for the game with a synthwave aesthetic and skin support."""

    def __init__(self, screen: pygame.Surface, board: "Board", skin: dict):
        self.screen = screen
        self.board = board
        self.skin = skin
        self._load_fonts()

    def _load_fonts(self) -> None:
        """Loads custom fonts, with a fallback to the default font."""
        custom_font_path = Path(config.CUSTOM_FONT_PATH)
        try:
            if not custom_font_path.exists():
                raise FileNotFoundError
            self.font_s = pygame.font.Font(custom_font_path, config.FONT_SIZE_S)
            self.font_m = pygame.font.Font(custom_font_path, config.FONT_SIZE_M)
            self.font_l = pygame.font.Font(custom_font_path, config.FONT_SIZE_L)
        except (pygame.error, FileNotFoundError):
            print(f"Warning: Custom font not found. Falling back to default.")
            self.font_s = pygame.font.Font(None, config.FONT_SIZE_S)
            self.font_m = pygame.font.Font(None, config.FONT_SIZE_M)
            self.font_l = pygame.font.Font(None, config.FONT_SIZE_L)
    
    def _draw_text(self, text: str, font: pygame.font.Font, color: tuple, center: tuple, shadow: bool = False):
        """Helper function to draw text with an optional shadow/background."""
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=center)

        if shadow:
            shadow_rect = text_rect.inflate(20, 10)
            shadow_surf = pygame.Surface(shadow_rect.size, pygame.SRCALPHA)
            shadow_surf.fill(self.skin["TEXT_SHADOW"])
            self.screen.blit(shadow_surf, shadow_rect.move(center[0] - shadow_rect.width / 2, center[1] - shadow_rect.height / 2))

        self.screen.blit(text_surf, text_rect)

    def _draw_grid(self) -> None:
        """Draws the grid with a glowing effect."""
        grid_surf = pygame.Surface((config.WIDTH, config.HEIGHT), pygame.SRCALPHA)
        for x in range(0, config.WIDTH, config.CELL_SIZE):
            pygame.draw.line(grid_surf, self.skin["GRID"], (x, 0), (x, config.HEIGHT))
        for y in range(0, config.HEIGHT, config.CELL_SIZE):
            pygame.draw.line(grid_surf, self.skin["GRID"], (0, y), (config.WIDTH, y))
        self.screen.blit(grid_surf, (0, 0))

    def _draw_snake(self, snake: "Snake") -> None:
        """Draws the snake with a glowing head and body."""
        for i, segment in enumerate(snake.body):
            x, y = segment
            rect = pygame.Rect(x * config.CELL_SIZE, y * config.CELL_SIZE, config.CELL_SIZE, config.CELL_SIZE)
            glow_rect = rect.inflate(4, 4)
            glow_surf = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
            
            color = self.skin["SNAKE_HEAD"] if i == 0 else self.skin["SNAKE_BODY"]
            
            pygame.draw.rect(glow_surf, self.skin["SNAKE_GLOW"], glow_surf.get_rect(), border_radius=5)
            self.screen.blit(glow_surf, glow_rect)
            pygame.draw.rect(self.screen, color, rect, border_radius=3)

    def _draw_food(self, food: "Food", ticks: int) -> None:
        """Draws the food with a pulsing glow effect."""
        x, y = food.position
        rect = pygame.Rect(x * config.CELL_SIZE, y * config.CELL_SIZE, config.CELL_SIZE, config.CELL_SIZE)
        
        # Pulsing effect for the glow
        pulse = (math.sin(ticks * 0.01) + 1) / 2  # Varies between 0 and 1
        glow_size = int(8 + pulse * 6)
        glow_rect = rect.inflate(glow_size, glow_size)
        glow_surf = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
        
        pygame.draw.rect(glow_surf, self.skin["FOOD_GLOW"], glow_surf.get_rect(), border_radius=10)
        self.screen.blit(glow_surf, glow_rect)
        pygame.draw.rect(self.screen, self.skin["FOOD"], rect, border_radius=5)

    def _draw_hud(self, score: int, high_score: int) -> None:
        """Draws the Heads-Up Display (Score and High Score)."""
        self._draw_text(f"Score: {score}", self.font_m, self.skin["TEXT"], (config.WIDTH * 0.25, 30))
        self._draw_text(f"High Score: {high_score}", self.font_m, self.skin["TEXT_ACCENT"], (config.WIDTH * 0.75, 30))

    def _draw_skin_preview(self, center: tuple):
        # Draw a mini grid and a mini snake for skin preview in the menu
        preview_size = 120
        cell = 15
        surf = pygame.Surface((preview_size, preview_size), pygame.SRCALPHA)
        # Draw grid
        for x in range(0, preview_size, cell):
            pygame.draw.line(surf, self.skin["GRID"], (x, 0), (x, preview_size))
        for y in range(0, preview_size, cell):
            pygame.draw.line(surf, self.skin["GRID"], (0, y), (preview_size, y))
        # Draw snake (3 segments)
        for i, (sx, sy) in enumerate([(4, 4), (3, 4), (2, 4)]):
            rect = pygame.Rect(sx * cell, sy * cell, cell, cell)
            glow_rect = rect.inflate(4, 4)
            glow_surf = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
            color = self.skin["SNAKE_HEAD"] if i == 0 else self.skin["SNAKE_BODY"]
            pygame.draw.rect(glow_surf, self.skin["SNAKE_GLOW"], glow_surf.get_rect(), border_radius=5)
            surf.blit(glow_surf, glow_rect)
            pygame.draw.rect(surf, color, rect, border_radius=3)
        # Draw food
        food_rect = pygame.Rect(6 * cell, 4 * cell, cell, cell)
        glow_rect = food_rect.inflate(8, 8)
        glow_surf = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, self.skin["FOOD_GLOW"], glow_surf.get_rect(), border_radius=10)
        surf.blit(glow_surf, glow_rect)
        pygame.draw.rect(surf, self.skin["FOOD"], food_rect, border_radius=5)
        # Blit preview to main screen
        rect = surf.get_rect(center=center)
        self.screen.blit(surf, rect)

    def _draw_main_menu(self, skin_name, skin_desc, controller_hint=None):
        """Draws the main menu screen."""
        self._draw_text("Slither.py", self.font_l, self.skin["SNAKE_HEAD"], (config.WIDTH / 2, config.HEIGHT / 8))
        self._draw_text("Press ENTER to Start", self.font_m, self.skin["TEXT"], (config.WIDTH / 2, config.HEIGHT / 2 + 120), shadow=True)
        self._draw_text("Press ESC to Quit", self.font_s, self.skin["TEXT"], (config.WIDTH / 2, config.HEIGHT / 2 + 170))
        # Skin selection with visible arrows
        skin_label = f"<   {skin_name}   >"
        self._draw_text(skin_label, self.font_m, self.skin["TEXT_ACCENT"], (config.WIDTH / 2, config.HEIGHT / 2 - 10))
        self._draw_text(skin_desc, self.font_s, self.skin["TEXT"], (config.WIDTH / 2, config.HEIGHT / 2 + 35))
        self._draw_text("Use ← / → to change skin", self.font_s, self.skin["TEXT"], (config.WIDTH / 2, config.HEIGHT / 2 + 70))
        # Move preview lower to avoid overlap
        self._draw_skin_preview((config.WIDTH / 2, config.HEIGHT / 2 - 100))
        if controller_hint:
            self._draw_text(controller_hint, self.font_s, self.skin["TEXT_ACCENT"], (config.WIDTH / 2, config.HEIGHT - 40))

    def _draw_paused_overlay(self) -> None:
        """Draws the paused screen overlay."""
        self._draw_text("PAUSED", self.font_l, self.skin["TEXT_ACCENT"], (config.WIDTH / 2, config.HEIGHT / 2), shadow=True)

    def _draw_game_over(self, score: int, high_score: int, is_new_high: bool) -> None:
        """Draws the game over screen."""
        self._draw_text("GAME OVER", self.font_l, self.skin["SNAKE_HEAD"], (config.WIDTH / 2, config.HEIGHT / 4))
        
        if is_new_high:
            self._draw_text("NEW HIGH SCORE!", self.font_m, self.skin["FOOD"], (config.WIDTH / 2, config.HEIGHT / 2 - 40))
        
        self._draw_text(f"Final Score: {score}", self.font_m, self.skin["TEXT"], (config.WIDTH / 2, config.HEIGHT / 2 + 20))
        self._draw_text(f"High Score: {high_score}", self.font_s, self.skin["TEXT"], (config.WIDTH / 2, config.HEIGHT / 2 + 60))
        
        self._draw_text("Press ENTER to Play Again", self.font_m, self.skin["TEXT"], (config.WIDTH / 2, config.HEIGHT * 3 / 4), shadow=True)

    def _draw_demo_overlay(self):
        self._draw_text("DEMO MODE — AI AUTOPLAY", self.font_l, self.skin["TEXT_ACCENT"], (config.WIDTH / 2, 100), shadow=True)
        self._draw_text("Press any key or button to return to menu", self.font_m, self.skin["TEXT"], (config.WIDTH / 2, 180))

    def draw(self, game_state: GameState, snake: "Snake", food: "Food", score: int, high_score: int, ticks: int, is_new_high: bool = False, skin_name: str = "", skin_desc: str = "", controller_hint: str = None):
        """Draws the entire game state to the screen."""
        self.screen.fill(self.skin["BACKGROUND"])
        
        if game_state == GameState.MAIN_MENU:
            self._draw_main_menu(skin_name, skin_desc, controller_hint)
        elif game_state == GameState.DEMO:
            self._draw_grid()
            self._draw_snake(snake)
            self._draw_food(food, ticks)
            self._draw_hud(score, high_score)
            self._draw_demo_overlay()
        else:
            # Draw game elements for PLAYING, PAUSED, and GAME_OVER states
            self._draw_grid()
            self._draw_snake(snake)
            self._draw_food(food, ticks)
            self._draw_hud(score, high_score)

            if game_state == GameState.PAUSED:
                self._draw_paused_overlay()
            elif game_state == GameState.GAME_OVER:
                self._draw_game_over(score, high_score, is_new_high)
            
        pygame.display.flip()