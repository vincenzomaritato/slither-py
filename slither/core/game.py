import pygame
from slither.core.board import Board
from slither.core.snake import Snake
from slither.core.food import Food
from slither.ui.renderer import Renderer
from slither.ui.sound import SoundManager
from slither import config
from slither.core.gamestate import GameState
from slither.core.score_manager import load_high_score, save_high_score
from slither.core.skin_manager import SkinManager
import random

def run_game():
    pygame.init()
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
    for js in joysticks:
        js.init()

    board = Board(config.WIDTH, config.HEIGHT, config.CELL_SIZE)
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    pygame.display.set_caption("Slither.py")
    skin_manager = SkinManager()
    skin = skin_manager.get_active_skin()
    renderer = Renderer(screen, board, skin)
    sound_manager = SoundManager()
    clock = pygame.time.Clock()
    
    def _reset_game_vars():
        """Resets all game variables for a new game."""
        snake = Snake(board)
        food = Food(board)
        food.respawn(snake)
        score = 0
        current_speed = config.FPS
        return snake, food, score, current_speed

    game_state = GameState.MAIN_MENU
    high_score = load_high_score()
    
    # Initialize game variables
    snake, food, score, current_speed = _reset_game_vars()
    is_new_high_score = False
    controller_hint = ""
    if joysticks:
        controller_hint = f"Controller detected: {joysticks[0].get_name()}"

    # Controller state
    last_hat = (0, 0)
    last_axis = (0, 0)
    
    demo_inactive_timer = 0
    DEMO_INACTIVITY_SECONDS = 15

    while game_state != None:
        ticks = pygame.time.get_ticks()
        skin = skin_manager.get_active_skin()
        renderer.skin = skin

        # --- Inactivity timer for auto-demo ---
        if game_state == GameState.MAIN_MENU:
            demo_inactive_timer += clock.get_time()
            if demo_inactive_timer > DEMO_INACTIVITY_SECONDS * 1000:
                game_state = GameState.DEMO
                demo_inactive_timer = 0
        else:
            demo_inactive_timer = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state = None

            # Controller/keyboard input resets inactivity timer
            if game_state == GameState.MAIN_MENU and event.type in (pygame.KEYDOWN, pygame.JOYBUTTONDOWN, pygame.JOYHATMOTION):
                demo_inactive_timer = 0

            # --- Controller input mapping ---
            if event.type == pygame.JOYHATMOTION:
                # D-Pad
                if game_state == GameState.PLAYING:
                    if event.value == (0, 1):
                        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP))
                    elif event.value == (0, -1):
                        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN))
                    elif event.value == (-1, 0):
                        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT))
                    elif event.value == (1, 0):
                        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT))
                elif game_state == GameState.MAIN_MENU:
                    if event.value == (1, 0):
                        skin_manager.next_skin()
                    elif event.value == (-1, 0):
                        skin_manager.prev_skin()
            if event.type == pygame.JOYBUTTONDOWN:
                # Button 0 (A/X): Start/Restart
                if event.button == 0:
                    if game_state == GameState.MAIN_MENU:
                        game_state = GameState.PLAYING
                    elif game_state == GameState.GAME_OVER:
                        snake, food, score, current_speed = _reset_game_vars()
                        is_new_high_score = False
                        game_state = GameState.PLAYING
                # Button 1 (B/O): Esc
                if event.button == 1:
                    if game_state in [GameState.MAIN_MENU, GameState.GAME_OVER]:
                        game_state = None
                # Button 7 (Start/Options): Pausa/Resume
                if event.button == 7:
                    if game_state == GameState.PLAYING:
                        game_state = GameState.PAUSED
                    elif game_state == GameState.PAUSED:
                        game_state = GameState.PLAYING

            # --- Keyboard input mapping (resto invariato) ---
            if game_state == GameState.MAIN_MENU:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_state = GameState.PLAYING
                    elif event.key == pygame.K_ESCAPE:
                        game_state = None
                    elif event.key == pygame.K_RIGHT:
                        skin_manager.next_skin()
                    elif event.key == pygame.K_LEFT:
                        skin_manager.prev_skin()
                    elif event.key == pygame.K_d:
                        game_state = GameState.DEMO
            elif game_state == GameState.PLAYING:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    game_state = GameState.PAUSED
                else:
                    snake.handle_event(event)
            elif game_state == GameState.PAUSED:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    game_state = GameState.PLAYING
            elif game_state == GameState.GAME_OVER:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Reset game
                        snake, food, score, current_speed = _reset_game_vars()
                        is_new_high_score = False
                        game_state = GameState.PLAYING
                    elif event.key == pygame.K_ESCAPE:
                        game_state = None
            elif game_state == GameState.DEMO:
                if event.type in (pygame.KEYDOWN, pygame.JOYBUTTONDOWN, pygame.JOYHATMOTION):
                    game_state = GameState.MAIN_MENU

        if game_state == GameState.PLAYING:
            snake.move()

            if snake.eats(food):
                snake.grow()
                food.respawn(snake)
                score += 10
                sound_manager.play_eat()
                # Increase speed every 50 points
                if score > 0 and score % 50 == 0:
                    current_speed += 1

            if snake.has_collided():
                game_state = GameState.GAME_OVER
                if score > high_score:
                    high_score = score
                    save_high_score(high_score)
                    is_new_high_score = True
                sound_manager.play_hit()
        elif game_state == GameState.DEMO:
            # Simple AI: move towards food, avoid walls
            head_x, head_y = snake.get_head()
            food_x, food_y = food.position
            dx = food_x - head_x
            dy = food_y - head_y
            # Prefer horizontal movement if not aligned
            if dx != 0:
                direction = (1 if dx > 0 else -1, 0)
            elif dy != 0:
                direction = (0, 1 if dy > 0 else -1)
            else:
                direction = snake.direction
            # Avoid 180° turn
            if (direction[0] != -snake.direction[0] or direction[1] != -snake.direction[1]):
                snake.direction = direction
            # Randomly try to avoid self-collision
            next_head = (head_x + snake.direction[0], head_y + snake.direction[1])
            if next_head in snake.body or not board.in_bounds(*next_head):
                # Try perpendicular directions
                for alt in [(-snake.direction[1], snake.direction[0]), (snake.direction[1], -snake.direction[0])]:
                    alt_head = (head_x + alt[0], head_y + alt[1])
                    if board.in_bounds(*alt_head) and alt_head not in snake.body:
                        snake.direction = alt
                        break
            snake.move()
            if snake.eats(food):
                snake.grow()
                food.respawn(snake)
            if snake.has_collided():
                # Restart demo
                snake, food, score, current_speed = _reset_game_vars()
                is_new_high_score = False

        # Drawing is now handled by the renderer
        renderer.draw(
            game_state, snake, food, score, high_score, ticks, is_new_high_score,
            skin_name=skin["name"], skin_desc=skin["description"],
            controller_hint=controller_hint
        )

        clock.tick(current_speed)

    pygame.quit()