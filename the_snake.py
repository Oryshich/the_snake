"""Питон из спринта №3."""
import sys
from random import randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


START_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

BLACK_COLOR = (0, 0, 0)
GRAY_COLOR = (93, 216, 228)
RED_COLOR = (255, 0, 0)
GREEN_COLOR = (0, 255, 0)

BOARD_BACKGROUND_COLOR = BLACK_COLOR

BORDER_COLOR = GRAY_COLOR

APPLE_COLOR = RED_COLOR

SNAKE_COLOR = GREEN_COLOR

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс."""

    def __init__(self, body_color=BOARD_BACKGROUND_COLOR,
                 position=START_POSITION):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод отрисовки (должен быть реализован в потомках)."""
        raise NotImplementedError(f'class method {self.__class__.__name__}.'
                                  'draw() must be redefined')

    def draw_rect(self, position=START_POSITION):
        """Отрисовка одной ячейки с тенью"""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Приз."""

    def __init__(self, apple_color=APPLE_COLOR, prohibition_positions=None):
        self.randomize_position(prohibition_positions=prohibition_positions)
        super().__init__(body_color=apple_color, position=self.position)

    def randomize_position(self, prohibition_positions=None):
        """Случайное расположение."""
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        while (prohibition_positions is not None and self.position in
               prohibition_positions):
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self):
        """Отрисовка яблока."""
        self.draw_rect(position=self.position)


class Snake(GameObject):
    """Питон."""

    def __init__(self, snake_color=SNAKE_COLOR):
        super().__init__(body_color=snake_color, position=START_POSITION)
        self.positions = [self.position]
        self.direction = RIGHT
        self.last = None

    def draw(self):
        """Отрисовка питона."""
        # Отрисовка головы змейки
        self.draw_rect(position=self.get_head_position)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self, new_direction=None):
        """Смена направления движения."""
        if new_direction:
            self.direction = new_direction

    def move(self):
        """Отработка движения питона."""
        add_x = GRID_SIZE * self.direction[0]
        add_y = GRID_SIZE * self.direction[1]

        new_x = (self.positions[0][0] + add_x) % SCREEN_WIDTH
        new_y = (self.positions[0][1] + add_y) % SCREEN_HEIGHT

        self.positions.insert(0, (new_x, new_y))
        self.last = self.positions.pop()

    @property
    def get_head_position(self):
        """Позиция головы питона."""
        return self.positions[0]

    @property
    def get_length(self):
        """Длина питона."""
        return len(self.positions)

    def reset(self):
        """Перезапуск питона."""
        self.positions = [self.position]
        self.direction = RIGHT
        self.last = None

    def increase_length(self):
        """Удлинение питона"""
        self.positions.append(self.positions[-1])


def handle_keys(game_object):
    """Обработка нажатия клавиш."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit(0)
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.update_direction(new_direction=UP)
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.update_direction(new_direction=DOWN)
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.update_direction(new_direction=LEFT)
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.update_direction(new_direction=RIGHT)
            elif event.key == pg.K_SPACE:
                game_object.positions.append(game_object.positions[-1])
            elif event.key == pg.K_ESCAPE:
                sys.exit(0)


def main():
    """Основной цикл игры."""
    pg.init()
    snake = Snake()
    apple = Apple(prohibition_positions=snake.positions)

    apple.draw()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        if (snake.get_head_position == apple.position):
            snake.increase_length()
            apple.randomize_position(prohibition_positions=snake.positions)
        elif snake.get_head_position in snake.positions[4:]:
            # Нельзя пересекать свое тело
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
