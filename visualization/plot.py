# Цветовая карта
import numpy as np
from matplotlib import colors
from model.cell import CellState


# Цвета: EMPTY=коричневый, TREE=зелёный, FIRE=красный/оранжевый, WATER=синий
COLORS = [(0.2, 0, 0), (0, 0.5, 0), (1, 0, 0), 'orange', 'blue']
BOUNDS = [0, 1, 2, 3, 4]

CMAP = colors.ListedColormap(COLORS)
NORM = colors.BoundaryNorm(BOUNDS, CMAP.N)
