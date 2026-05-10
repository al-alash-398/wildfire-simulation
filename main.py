# Точка входа. Запуск симуляции лесного пожара
from config import SimulationConfig
from model.grid import ForestGrid
from visualization.animate import run_animation


def main() -> None:
    # Запускает симуляцию с настройками по умолчанию
    config = SimulationConfig()
    grid = ForestGrid(config)

    # Озеро в центре
    grid.add_water(40, 40, 60, 60)

    # Поджигаем несколько точек для начала
    grid.grid[45, 65] = 4
    grid.grid[46, 65] = 4
    grid.grid[47, 65] = 4

    # Передаём config вторым аргументом
    run_animation(grid, config, frames=config.frames, interval=config.interval_ms)


if __name__ == "__main__":
    main()
