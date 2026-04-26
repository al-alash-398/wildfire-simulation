# Анимация распространения пожара
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.patches import Patch

from model.grid import ForestGrid
from visualization.plot import CMAP, NORM


def run_animation(grid: ForestGrid, frames: int = 200, interval: int = 100):
    # Запускает анимацию симуляции
    fig = plt.figure(figsize=(10, 6.25))
    ax = fig.add_subplot(111)
    ax.set_axis_off()
    im = ax.imshow(grid.grid, cmap=CMAP, norm=NORM)

    legend_elements = [
        Patch(facecolor=(0.2, 0, 0), label='Пустошь'),
        Patch(facecolor=(0, 0.5, 0), label='Дерево'),
        Patch(facecolor='red', label='Огонь'),
        Patch(facecolor='blue', label='Вода'),
    ]
    ax.legend(
        handles=legend_elements,
        loc='upper right',
        fontsize='small',
        framealpha=0.8,
    )

    def animate_fn(i: int) -> None:
        im.set_data(animate_fn.grid)
        animate_fn.grid = grid.step()

    animate_fn.grid = grid.grid

    anim = animation.FuncAnimation(
        fig, animate_fn, interval=interval, frames=frames
    )
    plt.show()
    return anim
