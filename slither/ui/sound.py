"""
This module contains the SoundManager for the Slither game.
"""

import pygame

class SoundManager:
    """Handles loading and playing sound effects."""

    def __init__(self):
        """Initializes the mixer and loads sounds."""
        pygame.mixer.init()
        try:
            self.eat_sound = pygame.mixer.Sound("assets/sounds/eat.mp3")
            self.hit_sound = pygame.mixer.Sound("assets/sounds/hit.mp3")
        except pygame.error as e:
            print(f"Warning: Could not load sound files: {e}")
            # Create dummy sound objects so the game doesn't crash
            self.eat_sound = pygame.mixer.Sound(buffer=b"")
            self.hit_sound = pygame.mixer.Sound(buffer=b"")

    def play_eat(self) -> None:
        """Plays the sound for eating food."""
        self.eat_sound.play()

    def play_hit(self) -> None:
        """Plays the sound for a collision."""
        self.hit_sound.play() 