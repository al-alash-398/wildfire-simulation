# Логика распространения огня

# Основана на модели Кристиана Хилла (2016):
# https://scipython.com/blog/the-forest-fire-model/

# Модификации:
# - Выделено в отдельный модуль
# - Добавлена поддержка направленного ветра
# - Добавлены проверки границ
# - Добавлена влажность
# - Добавлены типы деревьев с разной горючестью
# - Spotting (искры)


import numpy as np
from model.cell import CellState


# 8 соседей (окрестность Мура)
NEIGHBOR_OFFSETS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def count_burning_neighbors(
    grid: np.ndarray,
    x: int,
    y: int,
    wind_probs: tuple,
    diagonal_factor: float,
    humidity: float = 0.0,
    flammability: float = 1.0,
) -> int:

    # Считает, сколько соседей клетки (x, y) подожгут её на этом шаге

    # Учитывает:
    # - diagonal_factor - пониженная вероятность для диагоналей
    # - wind_probs - направление ветра
    # - humidity - влажность (0 = сухо, 1 = мокро)
    # - flammability - горючесть конкретного дерева (от 0 до 1)

    count = 0
    for idx, (dx, dy) in enumerate(NEIGHBOR_OFFSETS):
        nx, ny = x + dx, y + dy

        if nx < 0 or nx >= grid.shape[1] or ny < 0 or ny >= grid.shape[0]:
            continue
        if grid[ny, nx] != CellState.FIRE:
            continue
        if abs(dx) == abs(dy) and np.random.random() < diagonal_factor:
            continue
        if np.random.random() <= wind_probs[idx]:
            # Горючесть и влажность снижают вероятность
            if np.random.random() <= flammability * (1.0 - humidity):
                count += 1

    return count


def check_spotting(
    grid: np.ndarray,
    x: int,
    y: int,
    wind_probs: tuple,
    spotting_prob: float,
    spotting_distance: int,
) -> bool:

    # Проверяет, долетит ли искра до клетки (x, y).
    # Искры летят по направлению ветра на spotting_distance клеток.

    if np.random.random() >= spotting_prob:
        return False

    h, w = grid.shape

    for idx, (dx, dy) in enumerate(NEIGHBOR_OFFSETS):
        if wind_probs[idx] < 0.5:
            continue

        # Источник искры: на расстоянии spotting_distance против ветра
        sx = x - dx * spotting_distance
        sy = y - dy * spotting_distance

        if 0 <= sx < w and 0 <= sy < h and grid[sy, sx] == CellState.FIRE:
            return True

    return False

