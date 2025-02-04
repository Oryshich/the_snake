"""Питон из спринта №3"""
import pygame
from random import randint


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


CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject():
    """Базовый класс"""

    def __init__(self, body_color=APPLE_COLOR):
        self.position = None
        self.body_color = body_color

    def draw():
        """Метод отрисовки (должен быть реализован в потомках)"""
        pass


class Apple(GameObject):
    """Приз"""

    def __init__(self, prohibition_positions=None):
        super().__init__(APPLE_COLOR)
        self.position = self.randomize_position(prohibition_positions)

    def randomize_position(self, prohibition_positions=None):
        """Случайное расположение"""
        position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                    randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        if prohibition_positions is not None:
            while position in prohibition_positions:
                position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                            randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        return position

    def draw(self):
        """Отрисовка яблока"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Питон"""

    def __init__(self):
        super().__init__(SNAKE_COLOR)
        self.positions = []
        self.next_direction = None
        self.direction = RIGHT
        self.positions.append(CENTER)
        self.last = None

    def draw(self):
        """Отрисовка питона"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Смена направления движения"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Отработка движения питона"""
        new_item = (self.positions[0][0] + GRID_SIZE * self.direction[0],
                    self.positions[0][1] + GRID_SIZE * self.direction[1])
        self.positions.insert(0, new_item)
        if self.positions[0][0] == SCREEN_WIDTH:
            self.positions[0] = (0, self.positions[0][1])
        if self.positions[0][0] < 0:
            self.positions[0] = (SCREEN_WIDTH - GRID_SIZE,
                                 self.positions[0][1])
        if self.positions[0][1] == SCREEN_HEIGHT:
            self.positions[0] = (self.positions[0][0], 0)
        if self.positions[0][1] < 0:
            self.positions[0] = (self.positions[0][0],
                                 SCREEN_HEIGHT - GRID_SIZE)
        self.last = self.positions[-1]
        self.positions.pop()

    def get_head_position(self):
        """Позиция головы питона"""
        return self.positions[0]

    def get_length(self):
        """Длина питона"""
        return len(self.positions)

    def reset(self):
        """Перезапуск питона"""
        self.positions = []
        self.positions.append(CENTER)


def handle_keys(game_object):
    """Обработка нажатия клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pygame.K_SPACE:
                game_object.positions.append(game_object.positions[-1])


def main():
    """Основной цикл игры"""
    # Инициализация PyGame:
    pygame.init()
    snake = Snake()
    apple = Apple(snake.positions)

    apple.draw()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if (snake.positions[0] == apple.position):
            snake.positions.append(snake.positions[-1])
            apple.position = apple.randomize_position(snake.positions)
            apple.draw()
        if snake.positions[0] in snake.positions[3:]:
            # Нельзя пересекать свое тело
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, (0, 0,
                             SCREEN_WIDTH, SCREEN_HEIGHT))
            snake.reset()
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
