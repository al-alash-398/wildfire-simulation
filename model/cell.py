# Состояния клетки
from enum import IntEnum


class CellState(IntEnum):
    # Возможные состояния клетки

    EMPTY = 0   # пустошь
    TREE_PINE = 1  # сосна
    TREE_BIRCH = 2  # берёза
    TREE_OAK = 3  # дуб
    FIRE = 4 # огонь
    WATER = 5 # вода
