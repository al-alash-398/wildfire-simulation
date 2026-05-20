# Сетка леса и итерация
import numpy as np

from model.cell import CellState
from model.spread import count_burning_neighbors
from config import SimulationConfig
from model.spread import count_burning_neighbors, check_spotting
from numba import njit


class ForestGrid:

    # Сетка лесного пожара

    # Атрибуты:
    # grid: np.ndarray
    #    Двумерный массив состояний клеток
    # config: SimulationConfig
    #    Параметры симуляции

    def __init__(self, config: SimulationConfig | None = None) -> None:
        self.config = config or SimulationConfig()
        self.grid = self._initialize_grid()

    @property
    def size(self) -> tuple:
        # Размеры сетки (height, width)
        return self.grid.shape

    @property
    def tree_count(self) -> int:
        # Текущее количество деревьев
        return int(np.sum(self.grid == CellState.TREE))

    @property
    def fire_count(self) -> int:
        # Текущее количество горящих клеток
        return int(np.sum(self.grid == CellState.FIRE))

    @property
    def empty_count(self) -> int:
        # Текущее количество пустых клеток
        return int(np.sum(self.grid == CellState.EMPTY))

    def _initialize_grid(self) -> np.ndarray:
        # Создаёт начальную сетку с деревьями разных типов
        w, h = self.config.grid_width, self.config.grid_height
        grid = np.zeros((h, w), dtype=int)

        # Где будут деревья
        mask = np.random.random((h, w)) < self.config.initial_forest_fraction

        if mask.any():
            n_trees = mask.sum()
            tree_types = list(self.config.tree_distribution.keys())
            probs = list(self.config.tree_distribution.values())
            probs = [p / sum(probs) for p in probs]

            chosen = np.random.choice(tree_types, size=n_trees, p=probs)
            grid[mask] = chosen

        # Граница всегда пустая
        grid[0, :] = CellState.EMPTY
        grid[-1, :] = CellState.EMPTY
        grid[:, 0] = CellState.EMPTY
        grid[:, -1] = CellState.EMPTY

        return grid

    def add_water(self, x1: int, y1: int, x2: int, y2: int) -> None:
        # Добавляет водную преграду (прямоугольник)
        self.grid[y1:y2, x1:x2] = CellState.WATER

    def step(self) -> np.ndarray:

        # Один шаг симуляции с numba-ускорением

        # Возвращает:
        # np.ndarray
        #    Новое состояние сетки.

        w, h = self.config.grid_width, self.config.grid_height
        new_grid = np.zeros((h, w), dtype=np.int64)

        _step_numba(
            self.grid, new_grid,
            np.array(self.config.wind_probs, dtype=np.float64),
            self.config.diagonal_factor,
            self.config.humidity,
            self.config.tree_growth_prob,
            self.config.lightning_prob,
            self.config.spotting_prob,
            self.config.spotting_distance,
            self.config.tree_flammability[1],
            self.config.tree_flammability[2],
            self.config.tree_flammability[3],
        )

        self.grid = new_grid
        return self.grid


@njit(nopython=True)
def _step_numba(
    grid, new_grid, wind_probs, diagonal_factor, humidity,
    tree_growth_prob, lightning_prob, spotting_prob, spotting_distance,
    flam_pine, flam_birch, flam_oak,
):
    # Numba-ускоренный шаг симуляции.
    h, w = grid.shape
    neighbours = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

    for y in range(1, h - 1):
        for x in range(1, w - 1):
            current = grid[y, x]

            if current == 5:  # вода
                new_grid[y, x] = 5
                continue

            if current == 0:  # пустошь
                if np.random.random() <= tree_growth_prob:
                    r = np.random.random()
                    if r < 0.4:
                        new_grid[y, x] = 1   # сосна
                    elif r < 0.8:
                        new_grid[y, x] = 2   # береза
                    else:
                        new_grid[y, x] = 3   # дуб
                continue

            if current == 4:  # огонь
                new_grid[y, x] = 0  # пустошь
                continue

            # сосна, береза, дуб
            if current == 1:
                flam = flam_pine
            elif current == 2:
                flam = flam_birch
            else:
                flam = flam_oak

            burning = 0

            for idx in range(8):
                dx, dy = neighbours[idx]
                nx, ny = x + dx, y + dy

                if nx < 0 or nx >= w or ny < 0 or ny >= h:
                    continue
                if grid[ny, nx] != 4:
                    continue
                if abs(dx) == abs(dy) and np.random.random() < diagonal_factor:
                    continue
                if np.random.random() <= wind_probs[idx]:
                    if np.random.random() <= flam * (1.0 - humidity):
                        burning += 1

            if burning > 0:
                new_grid[y, x] = 4
            elif np.random.random() <= lightning_prob * flam:
                new_grid[y, x] = 4
            elif np.random.random() < spotting_prob:
                spotted = False
                for idx in range(8):
                    if wind_probs[idx] < 0.5:
                        continue
                    dx, dy = neighbours[idx]
                    sx = x - dx * spotting_distance
                    sy = y - dy * spotting_distance
                    if 0 <= sx < w and 0 <= sy < h and grid[sy, sx] == 4:
                        new_grid[y, x] = 4
                        spotted = True
                        break
                if not spotted:
                    new_grid[y, x] = current
            else:
                new_grid[y, x] = current