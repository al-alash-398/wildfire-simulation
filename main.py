# Точка входа. Запуск симуляции лесного пожара
from config import SimulationConfig
from model.grid import ForestGrid
from visualization.animate import run_animation


def main() -> None:
    # Запускает симуляцию с настройками по умолчанию
    config = SimulationConfig()
    grid = ForestGrid(config)

    # Добавляем водные преграды
    grid.add_water(30, 30, 50, 50)

    run_animation(grid, frames=config.frames, interval=config.interval_ms)


if __name__ == "__main__":
    main()
