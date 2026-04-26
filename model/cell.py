# Состояния клетки
from enum import IntEnum


class CellState(IntEnum):
    # Возможные состояния клетки

    EMPTY = 0   # пустошь
    TREE = 1    # дерево
    FIRE = 2    # огонь
    WATER = 3   # вода (преграда)
