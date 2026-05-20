# Точка входа. Запуск симуляции лесного пожара
from config import SimulationConfig
from model.grid import ForestGrid
from visualization.animate import run_animation
from visualization.stats import FireStatistics


def main() -> None:
    # Запускает симуляцию с настройками по умолчанию и сбором статистики
    config = SimulationConfig()
    grid = ForestGrid(config)

    # Озеро в центре
    grid.add_water(40, 40, 60, 60)

    # Поджигаем несколько точек для начала
    grid.grid[45, 65] = 4
    grid.grid[46, 65] = 4
    grid.grid[47, 65] = 4

    stats = FireStatistics()

    # Передаём config вторым аргументом
    run_animation(grid, config, stats, frames=config.frames, interval=config.interval_ms)

    # После закрытия окна — графики
    stats.summary()
    stats.plot()


if __name__ == "__main__":
    main()
