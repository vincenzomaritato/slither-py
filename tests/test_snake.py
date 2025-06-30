import pytest
from slither.core.board import Board
from slither.core.snake import Snake
from slither.core.food import Food


@pytest.fixture
def board() -> Board:
    return Board(width=600, height=400, cell_size=20)


@pytest.fixture
def snake(board: Board) -> Snake:
    return Snake(board)


def test_snake_initial_position(snake: Snake, board: Board) -> None:
    mid_x = board.cols // 2
    mid_y = board.rows // 2
    assert snake.get_head() == (mid_x, mid_y)
    assert len(snake.body) == 1


def test_snake_movement(snake: Snake) -> None:
    old_head = snake.get_head()
    snake.move()
    new_head = snake.get_head()
    assert new_head != old_head
    assert len(snake.body) == 1


def test_snake_growth(snake: Snake) -> None:
    snake.grow()
    snake.move()
    assert len(snake.body) == 2
    snake.move()
    assert len(snake.body) == 2  # No additional growth


def test_snake_self_collision(board: Board) -> None:
    s = Snake(board)
    s.body = [(5, 5), (5, 6), (6, 6), (6, 5), (5, 5)]  # Head collides with tail
    assert s.has_collided()


def test_snake_border_collision(board: Board) -> None:
    s = Snake(board)
    s.body = [(-1, 0)]  # Outside the grid
    assert s.has_collided()


def test_snake_eats_food(snake: Snake, board: Board) -> None:
    food = Food(board)
    food.position = snake.get_head()
    assert snake.eats(food)