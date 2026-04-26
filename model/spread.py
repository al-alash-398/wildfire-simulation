# Логика распространения огня

# Основана на модели Кристиана Хилла (2016):
# https://scipython.com/blog/the-forest-fire-model/

# Модификации:
# - Выделено в отдельный модуль
# - Добавлена поддержка направленного ветра
# - Добавлены проверки границ


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
) -> int:

    # Считает, сколько соседей клетки (x, y) подожгут её на этом шаге

    # Учитывает:
    # - вероятность воспламенения от соседа по диагонали (diagonal_factor)
    # - направление ветра (wind_probs)

    count = 0
    for idx, (dx, dy) in enumerate(NEIGHBOR_OFFSETS):
        nx, ny = x + dx, y + dy

        # Проверка границ
        if nx < 0 or nx >= grid.shape[1] or ny < 0 or ny >= grid.shape[0]:
            continue

        if grid[ny, nx] != CellState.FIRE:
            continue

        # Диагональный сосед загорается с меньшей вероятностью
        if abs(dx) == abs(dy) and np.random.random() < diagonal_factor:
            continue

        # Ветер: если случайное число меньше wind_prob - сосед поджигает
        if np.random.random() <= wind_probs[idx]:
            count += 1

    return count
