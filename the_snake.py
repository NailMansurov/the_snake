from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Вычесления количества блоков GRID на игровом поле
BOARD_BY_GRID = GRID_WIDTH * GRID_HEIGHT

# Глубина цвета:
DEPTH = 32

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки (FPS):
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, DEPTH)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс."""

    def __init__(self, body_color=(0, 0, 0)) -> None:
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw(self):
        """Отрисовка объекта на экране, абстрактный метод"""
        pass

    def paint_rect(self, surface, position, color, board_with=True):
        """Отрисовка прямоугольника"""
        rect = pygame.Rect(
            (position),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, color, rect)
        if board_with is True:
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, описывающий ЗМЕЙКУ и действия над ней."""

    length = 1
    positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
    direction = RIGHT
    next_direction = None

    def __init__(self) -> None:
        super().__init__(body_color=SNAKE_COLOR)

    def update_direction(self):
        """Обновление направления движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод, обновление позиции змейки"""
        current_x, current_y = self.get_head_position()
        dx, dy = self.direction
        self.positions.insert(
            0,
            (
                (current_x + (dx * GRID_SIZE)) % SCREEN_WIDTH,
                (current_y + (dy * GRID_SIZE)) % SCREEN_HEIGHT,
            ),
        )
        if len(self.positions) > (self.length + 1):
            self.positions.pop()

    def draw(self, surface):
        """Метод, отрисовка змейки."""
        for position in self.positions[:-1]:
            self.paint_rect(
                surface,
                (position[0], position[1]),
                self.body_color,
                True
            )

        self.paint_rect(surface, (self.positions[0]), self.body_color, True)

    def get_head_position(self):
        """Метод, возвращение позицию головы змейки"""
        return self.positions[0]

    def reset(self):
        """Метод, возвращение змейки в первоначальные положение и размер"""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None


class Apple(GameObject):
    """Класс, описывающий ЯБЛОКО и действия над ним."""

    def __init__(self):
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Случайное положение яблока на игровом поле"""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, surface):
        """Отрисовка яблока на игровом поле"""
        self.paint_rect(
            surface,
            (self.position[0], self.position[1]),
            self.body_color,
            True
        )


def handle_keys(game_object):
    """Функция обработки нашатий клавиш для изменения движения змейки"""
    TURNS = {
        pygame.K_UP: (UP, DOWN),
        pygame.K_DOWN: (DOWN, UP),
        pygame.K_RIGHT: (RIGHT, LEFT),
        pygame.K_LEFT: (LEFT, RIGHT)
    }

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if (event.key in TURNS
                    and game_object.direction != TURNS[event.key][1]):
                game_object.next_direction = TURNS[event.key][0]


def main():
    """Создание экземляров классов Apple и Snake"""
    apple = Apple()
    snake = Snake()

    while True:
        """Основная логика игры"""
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Если змейка съела яблоко
        if snake.get_head_position() == apple.position:
            # Проверка, занимает ли змейка все игровое
            if (snake.length + 1) < BOARD_BY_GRID:
                snake.length += 1
                apple.randomize_position()
                # Проверка положения яблока относительно положения змейки:
                # если яблоко вновь в змейке - повторяем randomize_position()
                if apple.position in snake.positions:
                    while apple.position in snake.positions:
                        apple.randomize_position()
                        continue
            # Если для нового яблока нет места - перезапуск
            else:
                snake.reset()

        # Если змейка столкнётся сама с собой
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
