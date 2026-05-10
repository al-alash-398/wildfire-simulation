# Тесты для модуля распространения огня
import numpy as np
from model.cell import CellState
from model.spread import count_burning_neighbors, check_spotting


def test_humidity_blocks_fire():
    # При влажности 1.0 огонь не распространяется
    grid = np.zeros((5, 5), dtype=int)
    grid[2, 1] = CellState.FIRE
    wind = (1.0,) * 8
    for _ in range(100):
        count = count_burning_neighbors(
            grid, x=2, y=2, wind_probs=wind,
            diagonal_factor=1.0, humidity=1.0, flammability=1.0,
        )
        assert count == 0


def test_spotting_triggers():
    # Spotting с prob=1.0 всегда срабатывает
    grid = np.zeros((10, 10), dtype=int)
    grid[5, 3] = CellState.FIRE
    wind = (1.0,) * 8
    for _ in range(50):
        result = check_spotting(
            grid, x=5, y=5, wind_probs=wind,
            spotting_prob=1.0, spotting_distance=2,
        )
        assert result is True


def test_diagonal_factor_blocks():
    # diagonal_factor=1.0 блокирует диагональных соседей
    grid = np.zeros((5, 5), dtype=int)
    grid[1, 1] = CellState.FIRE
    wind = (1.0,) * 8
    for _ in range(50):
        count = count_burning_neighbors(
            grid, x=2, y=2, wind_probs=wind,
            diagonal_factor=1.0, humidity=0.0, flammability=1.0,
        )
        assert count == 0


def test_flammability():
    # Дуб горит реже сосны
    grid = np.zeros((5, 5), dtype=int)
    grid[2, 1] = CellState.FIRE
    wind = (1.0,) * 8

    counts_oak = []
    for _ in range(200):
        c = count_burning_neighbors(grid, 2, 2, wind, 1.0, 0.0, 0.3)
        counts_oak.append(c)

    counts_pine = []
    for _ in range(200):
        c = count_burning_neighbors(grid, 2, 2, wind, 1.0, 0.0, 1.0)
        counts_pine.append(c)

    assert np.mean(counts_oak) < np.mean(counts_pine)


if __name__ == "__main__":
    test_humidity_blocks_fire()
    print("OK test_humidity_blocks_fire")
    test_spotting_triggers()
    print("OK test_spotting_triggers")
    test_diagonal_factor_blocks()
    print("OK test_diagonal_factor_blocks")
    test_flammability()
    print("OK test_flammability")
    print("\nВсе тесты пройдены!")