# Статистика симуляции: графики деревья/огонь/пустошь
import matplotlib.pyplot as plt
import numpy as np
from model.cell import CellState


class FireStatistics:
    # Собирает и отображает статистику по шагам симуляции

    def __init__(self) -> None:
        self._history: list[dict] = []

    def record(self, grid: np.ndarray) -> None:
        # Записывает состояние сетки на текущем шаге
        self._history.append({
            'pine': int(np.sum(grid == CellState.TREE_PINE)),
            'birch': int(np.sum(grid == CellState.TREE_BIRCH)),
            'oak': int(np.sum(grid == CellState.TREE_OAK)),
            'fire': int(np.sum(grid == CellState.FIRE)),
            'empty': int(np.sum(grid == CellState.EMPTY)),
            'water': int(np.sum(grid == CellState.WATER)),
        })

    def plot(self) -> None:
        # Рисует графики статистики
        if not self._history:
            print("Нет данных")
            return

        steps = range(len(self._history))
        pine = [h['pine'] for h in self._history]
        birch = [h['birch'] for h in self._history]
        oak = [h['oak'] for h in self._history]
        fire = [h['fire'] for h in self._history]
        empty = [h['empty'] for h in self._history]
        total_trees = [p + b + o for p, b, o in zip(pine, birch, oak)]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        # График 1: деревья + огонь
        ax1.plot(steps, total_trees, 'green', linewidth=2, label='Все деревья')
        ax1.plot(steps, pine, 'darkgreen', linestyle='--', alpha=0.7, label='Сосны')
        ax1.plot(steps, birch, 'lightgreen', linestyle='--', alpha=0.7, label='Берёзы')
        ax1.plot(steps, oak, 'olive', linestyle='--', alpha=0.7, label='Дубы')
        ax1.plot(steps, fire, 'red', linewidth=2, label='Огонь')
        ax1.set_xlabel('Шаг')
        ax1.set_ylabel('Клеток')
        ax1.set_title('Деревья и огонь')
        ax1.legend(fontsize=8)
        ax1.grid(True, alpha=0.3)

        # График 2: пустошь
        ax2.plot(steps, empty, 'brown', linewidth=2, label='Пустошь')
        ax2.set_xlabel('Шаг')
        ax2.set_ylabel('Клеток')
        ax2.set_title('Выгоревшая площадь')
        ax2.legend(fontsize=8)
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()

    def summary(self) -> None:
        # Выводит сводку в консоль
        if not self._history:
            print("Нет данных")
            return

        first = self._history[0]
        last = self._history[-1]
        max_fire = max(h['fire'] for h in self._history)
        max_step = next(i for i, h in enumerate(self._history) if h['fire'] == max_fire)

        print(f"Начало: {first['pine'] + first['birch'] + first['oak']} деревьев, {first['fire']} огня")
        print(f"Конец:  {last['pine'] + last['birch'] + last['oak']} деревьев, {last['fire']} огня")
        print(f"Пик огня: {max_fire} на шаге {max_step}")