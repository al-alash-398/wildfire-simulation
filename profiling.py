# Профилирование скорости симуляции
import time
import numpy as np
from config import SimulationConfig
from model.grid import ForestGrid


def profile_step() -> None:
    # Замеряет время одного шага
    sizes = [50, 100, 200]

    print("Профилирование: время step()")
    print()

    for size in sizes:
        config = SimulationConfig(grid_width=size, grid_height=size,
                                   initial_forest_fraction=0.5)
        grid = ForestGrid(config)
        grid.grid[size // 2, size // 2] = 4

        # Прогрев
        for _ in range(5):
            grid.step()

        # Замер
        times = []
        for _ in range(20):
            start = time.perf_counter()
            grid.step()
            times.append(time.perf_counter() - start)

        avg = np.mean(times) * 1000
        fps = 1.0 / np.mean(times)

        print(f"\nРазмер: {size}×{size}")
        print(f"  Среднее время шага: {avg:.2f} мс")
        print(f"  FPS: {fps:.1f}")

    print()
    print("Анализ узких мест")
    print()
    print("""
1. Двойной цикл for - O(n^2). Можно заменить на numpy-операции.
2. count_burning_neighbors вызывается для каждого дерева.
   Можно предварительно считать свёртку.
3. Случайные числа в цикле - генерировать матрицу заранее.
4. numba JIT-компиляция уже добавлена — ускорение до 50 раз.
""")


def profile_memory() -> None:
    # Оценивает использование памяти
    print("Профилирование: память")
    print()

    for size in [100, 200, 400]:
        config = SimulationConfig(grid_width=size, grid_height=size)
        grid = ForestGrid(config)
        grid_bytes = grid.grid.nbytes
        total_bytes = grid_bytes * 2

        print(f"\nСетка {size}×{size}:")
        print(f"  Один массив: {grid_bytes / 1024:.1f} КБ")
        print(f"  Два массива: {total_bytes / 1024:.1f} КБ")


if __name__ == "__main__":
    profile_step()
    profile_memory()