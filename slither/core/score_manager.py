"""
This module handles loading and saving the high score.
"""

from pathlib import Path

HIGHSCORE_FILE = Path("highscore.txt")

def load_high_score() -> int:
    """
    Loads the high score from the file.

    Returns:
        The high score, or 0 if the file doesn't exist or is invalid.
    """
    if not HIGHSCORE_FILE.exists():
        return 0
    try:
        return int(HIGHSCORE_FILE.read_text())
    except (ValueError, IOError):
        return 0

def save_high_score(score: int) -> None:
    """
    Saves the new high score to the file.

    Args:
        score: The new high score to save.
    """
    try:
        HIGHSCORE_FILE.write_text(str(score))
    except IOError as e:
        print(f"Warning: Could not save high score: {e}") 