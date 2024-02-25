import random, pygame, sys
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_UP,
    K_DOWN,
    K_a,
    K_d,
    K_w,
    K_s,
    KEYDOWN,
    K_ESCAPE,
)
from colors import GREEN, RED, BLACK, WHITE

FPS = 15

win_witdh = 600
win_height = 600
cell_size = 15

no_cell_x = win_witdh // cell_size
no_cell_y = win_height // cell_size


RIGHT = "right"
LEFT = "left"
UP = "up"
DOWN = "down"


def main():
    global screen, font, clock

    pygame.init()
    screen = pygame.display.set_mode((win_witdh, win_height))
    pygame.display.set_caption("Snake")
    font = pygame.font.SysFont("timesnewromanboldttf", 18)
    clock = pygame.time.Clock()

    while True:
        game()


def game():
    snake_coords = [(0, 0)]
    direction = RIGHT

    apple_cell = get_apple_cell(snake_coords)

    while True:
        head_snake_cell = snake_coords[-1]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key in (K_LEFT, K_a) and direction != RIGHT:
                    direction = LEFT
                elif event.key in (K_RIGHT, K_d) and direction != LEFT:
                    direction = RIGHT
                elif event.key in (K_UP, K_w) and direction != DOWN:
                    direction = UP
                elif event.key in (K_DOWN, K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        if collision(snake_coords):
            return
        elif check_apple_eating(apple_cell, head_snake_cell):
            apple_cell = get_apple_cell(snake_coords)
        else:
            del snake_coords[0]

        if direction == UP:
            new_head = (head_snake_cell[0] - 1, head_snake_cell[1])
        elif direction == DOWN:
            new_head = (head_snake_cell[0] + 1, head_snake_cell[1])
        elif direction == LEFT:
            new_head = (head_snake_cell[0], head_snake_cell[1] - 1)
        elif direction == RIGHT:
            new_head = (head_snake_cell[0], head_snake_cell[1] + 1)

        snake_coords.append(new_head)

        screen.fill(BLACK)
        draw_snake(snake_coords)
        show_apple(apple_cell)
        show_score((len(snake_coords) - 1) * 5)
        pygame.display.update()
        clock.tick(FPS)


def get_random_cell():
    return (random.randint(0, no_cell_y - 1), random.randint(0, no_cell_x - 1))


def get_apple_cell(snake_cells):
    apple_cell = get_random_cell()

    while apple_cell in snake_cells:
        apple_cell = get_random_cell()

    return apple_cell


def show_apple(apple_cell):
    cell_y, cell_x = apple_cell

    pygame.draw.circle(
        screen,
        RED,
        (
            (cell_x * cell_size) + (cell_size // 2),
            (cell_y * cell_size) + (cell_size // 2),
        ),
        cell_size // 2,
    )


def collision(snake_coords):
    head = snake_coords[-1]
    if head in snake_coords[:-1]:
        return True

    if head[0] == -1 or head[0] == no_cell_y or head[1] == -1 or head[1] == no_cell_x:
        return True

    return False


def check_apple_eating(apple_cell, snake_head_cell):
    if apple_cell == snake_head_cell:
        return True
    return False


def draw_snake(snake_cells):
    for cell in snake_cells:
        cell_x = cell[1]
        cell_y = cell[0]

        pygame.draw.circle(
            screen,
            GREEN,
            (
                (cell_x * cell_size) + (cell_size // 2),
                (cell_y * cell_size) + (cell_size // 2),
            ),
            cell_size // 2,
        )


def show_score(score):
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (0, win_height - 20))


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()