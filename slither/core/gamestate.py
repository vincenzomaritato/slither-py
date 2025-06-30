"""
This module defines the possible states of the game.
"""

from enum import Enum, auto

class GameState(Enum):
    """Enumeration for game states."""
    MAIN_MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()
    DEMO = auto() 