import pygame
from typing import List, Tuple, TYPE_CHECKING
from slither.core.board import Board

if TYPE_CHECKING:
    from slither.core.food import Food

DIRECTIONS = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0)
}

class Snake:
    """Represents the snake in the Snake game."""
    
    def __init__(self, board: Board) -> None:
        """
        Initialize the snake at the center of the board.

        Args:
            board (Board): The game board.
        """
        self.board = board
        mid_x = board.cols // 2
        mid_y = board.rows // 2
        self.body: List[Tuple[int, int]] = [(mid_x, mid_y)]
        self.direction: Tuple[int, int] = (1, 0)
        self.pending_growth: int = 0
        
    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handle user input to change the snake's direction.

        Args:
            event (pygame.event.Event): The Pygame event to process.
        """
        if event.type == pygame.KEYDOWN:
            if event.key in DIRECTIONS:
                new_dir = DIRECTIONS[event.key]
                # Prevent 180° turn
                if (new_dir[0] != -self.direction[0] or new_dir[1] != -self.direction[1]):
                    self.direction = new_dir
    
    def move(self) -> None:
        """Move the snake in the current direction."""
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        
        self.body.insert(0, new_head)
        
        if self.pending_growth > 0:
            self.pending_growth -= 1
        else:
            self.body.pop()
            
    def grow(self) -> None:
        """Grow the snake by one segment."""
        self.pending_growth += 1
    
    def get_head(self) -> Tuple[int, int]:
        """
        Get the current head position.

        Returns:
            Tuple[int, int]: The (x, y) coordinates of the head.
        """
        return self.body[0]
    
    def has_collided(self) -> bool:
        """Check if the snake has collided with itself or the board boundaries.

        Returns:
            bool: True if collision occorred.
        """
        head = self.get_head()
        if not self.board.in_bounds(*head):
            return True
        return head in self.body[1:]
    
    def eats(self, food: "Food") -> bool:
        """
        Check if the snake eats the given food.

        Args:
            food (Food): The food to check collision with.

        Returns:
            bool: True if the snake eats the food.
        """
        return self.get_head() == food.position