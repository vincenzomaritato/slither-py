import random
from typing import Tuple, TYPE_CHECKING
from slither.core.board import Board

if TYPE_CHECKING:
    from slither.core.snake import Snake

class Food:
    """Represents the food that the snake can eat."""
    
    def __init__(self, board: Board) -> None:
        """
        Initialize the food.

        Args:
            board (Board): The game board.
        """
        self.board = board
        self.position: Tuple[int, int] = (0, 0)

    def respawn(self, snake: "Snake") -> None:
        """
        Generate a new random position for the food,
        making sure it's not on the snake.
        """
        free_cells = [
            (x, y)
            for x in range(self.board.cols)
            for y in range(self.board.rows)
            if (x, y) not in snake.body
        ]
        if free_cells:
            self.position = random.choice(free_cells)
        else:
            self.position = (-1, -1) # No space left