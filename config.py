# Конфигурация симуляции лесного пожара
from dataclasses import dataclass, field
from typing import Tuple, Dict


@dataclass
class SimulationConfig:
    # Параметры симуляции

    # Размер сетки
    grid_width: int = 100
    grid_height: int = 100

    # Вероятности
    tree_growth_prob: float = 0.05      # p - рост нового дерева
    lightning_prob: float = 0.0001      # f - удар молнии
    initial_forest_fraction: float = 0.2  # начальная доля деревьев

    # Ветер (вероятности для 8 соседей)
    #           NW  N  NE  W  E  SW  S  SE
    wind_probs: Tuple[float, ...] = (0.1, 0.1, 0.1, 0.1, 1.0, 0.1, 1.0, 1.0)

    # Диагональный фактор (площадь перекрытия кругов)
    diagonal_factor: float = 0.573

    # Новые параметры:
    humidity: float = 0.5 # влажность
    spotting_prob: float = 0.02 # вероятность искры
    spotting_distance: int = 2 # расстояние искры

    # Горючесть (вероятность возгорания)
    tree_flammability: Dict[int, float] = field(default_factory=lambda: {
        1: 1.0,  # сосна
        2: 0.6,  # берёза
        3: 0.3,  # дуб
    })

    # Распределение деревьев (вероятность того, что дерево будет некоторого вида)
    tree_distribution: Dict[int, float] = field(default_factory=lambda: {
        1: 0.4,  # сосна 40%
        2: 0.4,  # берёза 40%
        3: 0.2,  # дуб 20%
    })

    # Количество кадров анимации
    frames: int = 200
    interval_ms: int = 100

    # Задать влажность
    def set_humidity(self, value: float) -> None:
        self.humidity = max(0.0, min(1.0, value))

    # Задать направление ветра
    def set_wind_direction(self, direction: str) -> None:
        directions = {
            'N': (0.1, 1.0, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1),
            'S': (0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 1.0, 0.1),
            'E': (0.1, 0.1, 0.1, 0.1, 1.0, 0.1, 0.1, 0.1),
            'W': (0.1, 0.1, 0.1, 1.0, 0.1, 0.1, 0.1, 0.1),
            'NE': (0.1, 1.0, 0.1, 0.1, 1.0, 0.1, 0.1, 0.1),
            'NW': (1.0, 0.1, 0.1, 1.0, 0.1, 0.1, 0.1, 0.1),
            'SE': (0.1, 0.1, 0.1, 0.1, 1.0, 0.1, 1.0, 0.1),
            'SW': (0.1, 0.1, 0.1, 1.0, 0.1, 1.0, 0.1, 0.1),
            'none': (0.5,) * 8,
        }
        self.wind_probs = directions.get(direction, self.wind_probs)

    # Задать искры
    def set_spotting(self, prob: float, distance: int) -> None:
        self.spotting_prob = max(0.0, min(1.0, prob))
        self.spotting_distance = max(1, distance)
