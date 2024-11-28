from random import choice, randint

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
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption("Змейка")

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс игрового объекта."""

    def __init__(self, body_color=None) -> None:
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color

    def draw(self):
        """Отрисовки объекта на игровом поле."""
        raise NotImplementedError(
            f'В {self.__class__.__name__} '
            'необходимо переопределить метод draw()'
        )

    def rect_draw(self, position):
        """Отрисовка тела объекта."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Объект яблоко."""

    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color)
        self.randomize_position([self.position])

    def randomize_position(self, positions=None):
        """Устанавливает случайное положение яблока на игровом поле."""
        while True:
            self.position = (
                choice(range(0, GRID_WIDTH - 1)) * GRID_SIZE,
                choice(range(0, GRID_HEIGHT - 1)) * GRID_SIZE,
            )
            if self.position not in positions:
                break

    def draw(self):
        """Метод draw класса Apple."""
        self.rect_draw(self.position)


class Snake(GameObject):
    """Объект змейка."""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color)
        self.reset(direction=RIGHT)
        self.next_direction = None
        self.last = None

    def update_direction(self, next_direction=None):
        """Обновляет направление движения змейки."""
        if next_direction:
            self.direction = next_direction

    def move(self):
        """Обновляет позицию змейки."""
        head_cord_x, head_cord_y = self.get_head_position()
        direction_coord_x, direction_coord_y = self.direction
        new_x = (head_cord_x + direction_coord_x * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_cord_y + direction_coord_y * GRID_SIZE) % SCREEN_HEIGHT
        self.positions.insert(0, (new_x, new_y))
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self):
        """Отрисовывает змейку на экране."""
        for position in self.positions[:-1]:
            self.rect_draw(position)

        # Отрисовка головы змейки
        self.rect_draw(self.get_head_position())

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self, direction=None):
        """Сбрасывает змейку в начальное состояние."""
        self.direction = direction
        self.positions = []
        self.positions.append(((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)))
        self.length = len(self.positions)
        trend = [UP, DOWN, LEFT, RIGHT]
        if self.direction is None:
            self.direction = trend[randint(0, 3)]


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    action = {
        (pg.K_UP, RIGHT): UP,
        (pg.K_UP, LEFT): UP,
        (pg.K_DOWN, RIGHT): DOWN,
        (pg.K_DOWN, LEFT): DOWN,
        (pg.K_LEFT, UP): LEFT,
        (pg.K_LEFT, DOWN): LEFT,
        (pg.K_RIGHT, UP): RIGHT,
        (pg.K_RIGHT, DOWN): RIGHT
    }

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                pg.quit()
                raise SystemExit

            current_action = (event.key, game_object.direction)
            if current_action in action:
                game_object.next_direction = action.get(current_action)


def main():
    """Основной цикл игры."""
    pg.init()
    snake = Snake()
    apple = Apple()
    """Комментарий для ревьюера.
    Яблоко не может появится внутри змейки,
    тк в конструкторе Apple().__init__()
    вызывается метод randomize_position([self.position]),
    где self.position берется из родительского класса
    и равен точке появления змейки."""

    while True:
        clock.tick(SPEED)
        handle_keys(snake)

        snake.update_direction(snake.next_direction)
        snake.move()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)
            screen.fill(BOARD_BACKGROUND_COLOR)
            continue

        if apple.position == snake.get_head_position():
            apple.randomize_position(snake.positions)
            snake.length += 1

        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == "__main__":
    main()
