# Сетка леса и итерация
import numpy as np

from model.cell import CellState
from model.spread import count_burning_neighbors
from config import SimulationConfig
from model.spread import count_burning_neighbors, check_spotting


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

        # Один шаг симуляции.

        # Возвращает:
        # np.ndarray
        #    Новое состояние сетки.

        w, h = self.config.grid_width, self.config.grid_height
        new_grid = np.zeros((h, w), dtype=int)

        for y in range(1, h - 1):
            for x in range(1, w - 1):
                current = self.grid[y, x]

                # Вода не меняется
                if current == CellState.WATER:
                    new_grid[y, x] = CellState.WATER

                # Пустая клетка - может вырасти дерево
                elif current == CellState.EMPTY:
                    if np.random.random() <= self.config.tree_growth_prob:
                        tree_types = list(self.config.tree_distribution.keys())
                        probs = list(self.config.tree_distribution.values())
                        probs = [p / sum(probs) for p in probs]
                        new_grid[y, x] = np.random.choice(tree_types, p=probs)

                # Дерево может загореться
                elif current in (
                        CellState.TREE_PINE,
                        CellState.TREE_BIRCH,
                        CellState.TREE_OAK,
                ):
                    flammability = self.config.tree_flammability.get(current, 1.0)

                    burning = count_burning_neighbors(
                        self.grid, x, y,
                        self.config.wind_probs,
                        self.config.diagonal_factor,
                        humidity=self.config.humidity,
                        flammability=flammability,
                    )

                    if burning > 0:
                        new_grid[y, x] = CellState.FIRE
                    elif (
                            np.random.random()
                            <= self.config.lightning_prob * flammability
                    ):
                        new_grid[y, x] = CellState.FIRE
                    elif check_spotting(
                            self.grid, x, y,
                            self.config.wind_probs,
                            self.config.spotting_prob,
                            self.config.spotting_distance,
                    ):
                        new_grid[y, x] = CellState.FIRE
                    else:
                        new_grid[y, x] = current

                # Горящая клетка становится пустой
                elif current == CellState.FIRE:
                    new_grid[y, x] = CellState.EMPTY

        self.grid = new_grid
        return self.grid
