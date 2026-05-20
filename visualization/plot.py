# Цветовая карта
import numpy as np
from matplotlib import colors
from model.cell import CellState


COLORS = [
    (0.4, 0.3, 0.1),    # пустошь
    (0.0, 0.4, 0.0),    # сосна - тёмно-зелёный
    (0.2, 0.6, 0.2),    # берёза - светло-зелёный
    (0.1, 0.3, 0.1),    # дуб - очень тёмный
    (1.0, 0.0, 0.0),    # огонь - красный
    (0.1, 0.3, 0.8),    # вода - синий
]
BOUNDS = [0, 1, 2, 3, 4, 5, 6]

CMAP = colors.ListedColormap(COLORS)
NORM = colors.BoundaryNorm(BOUNDS, CMAP.N)
