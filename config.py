# Конфигурация симуляции лесного пожара
from dataclasses import dataclass
from typing import Tuple


@dataclass
class SimulationConfig:
    # Параметры симуляции

    # Размер сетки
    grid_width: int = 100
    grid_height: int = 100

    # Вероятности
    tree_growth_prob: float = 0.05      # p — рост нового дерева
    lightning_prob: float = 0.0001      # f — удар молнии
    initial_forest_fraction: float = 0.2  # начальная доля деревьев

    # Ветер (вероятности для 8 соседей)
    #           NW  N  NE  W  E  SW  S  SE
    wind_probs: Tuple[float, ...] = (0.1, 0.1, 0.1, 0.1, 1.0, 0.1, 1.0, 1.0)

    # Диагональный фактор (площадь перекрытия кругов)
    diagonal_factor: float = 0.573

    # Количество кадров анимации
    frames: int = 200
    interval_ms: int = 100
