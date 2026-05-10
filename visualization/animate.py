# Анимация распространения пожара
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.patches import Patch
from matplotlib.animation import FuncAnimation
from model.grid import ForestGrid
from visualization.plot import CMAP, NORM


def run_animation(grid: ForestGrid, config, stats=None, frames: int = 200, interval: int = 100) -> FuncAnimation:
    # Запускает анимацию симуляции
    fig = plt.figure(figsize=(12, 6.5))
    ax = fig.add_subplot(111)
    ax.set_axis_off()
    im = ax.imshow(grid.grid, cmap=CMAP, norm=NORM)

    # Легенда
    legend_elements = [
        Patch(facecolor=(0.4, 0.3, 0.1), label='Пустошь'),
        Patch(facecolor=(0.0, 0.4, 0.0), label='Сосна'),
        Patch(facecolor=(0.2, 0.6, 0.2), label='Берёза'),
        Patch(facecolor=(0.1, 0.3, 0.1), label='Дуб'),
        Patch(facecolor='red', label='Огонь'),
        Patch(facecolor='blue', label='Вода'),
    ]
    ax.legend(
        handles=legend_elements,
        loc='upper right',
        fontsize='small',
        framealpha=0.8,
    )
    # Текст
    info_text = ax.text(0.02, 0.98, '', transform=ax.transAxes,
                        fontsize=10, verticalalignment='top',
                        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    def update_info() -> None:
        info = (
            f"Влажность: {config.humidity:.1f} | "
            f"Spotting: {config.spotting_prob:.2f}/{config.spotting_distance} | "
            f"Шаг: {animate_fn.frame}"
        )
        info_text.set_text(info)

    def on_key(event) -> None:
        if event.key == 'up': # стрелка вверх
            config.set_humidity(config.humidity + 0.1) # увеличить влажность
        elif event.key == 'down': # стрелка вниз
            config.set_humidity(config.humidity - 0.1) # уменьшить влажность
        elif event.key == '1': # клавиша 1
            config.set_wind_direction('N') # ветер на север
        elif event.key == '2':
            config.set_wind_direction('NE') # ветер на северо-восток
        elif event.key == '3':
            config.set_wind_direction('E') # ветер на восток
        elif event.key == '4':
            config.set_wind_direction('SE') # ветер на юго-восток
        elif event.key == '5':
            config.set_wind_direction('S') # ветер на юг
        elif event.key == '6':
            config.set_wind_direction('SW') # ветер на юго-запад
        elif event.key == '7':
            config.set_wind_direction('W') # ветер на запад
        elif event.key == '8':
            config.set_wind_direction('NW') # ветер на северо-запад
        elif event.key == '0':
            config.set_wind_direction('none') # нет ветра
        elif event.key == 'left': # стрелка влево
            config.set_spotting(config.spotting_prob + 0.05, config.spotting_distance) # увеличить вероятность искры
        elif event.key == 'right': # стрелка вправо
            config.set_spotting(max(0, config.spotting_prob - 0.05), config.spotting_distance) # меньше вероятность искр
        update_info() # обновить

    fig.canvas.mpl_connect('key_press_event', on_key)

    def animate_fn(i: int, stats) -> None:
        animate_fn.frame = i

        if stats is not None:
            stats.record(animate_fn.grid) # записываем текущее состояние

        # Обновляем картинку
        im.set_data(animate_fn.grid)
        animate_fn.grid = grid.step()

        if i % 10 == 0:
            update_info()

    animate_fn.frame = 0 # счетчик кадров
    animate_fn.grid = grid.grid
    update_info()

    anim = animation.FuncAnimation(
        fig, animate_fn, interval=interval, frames=frames,
        fargs=(stats,)
    )
    animate_fn.anim = anim
    plt.show()
    return anim
