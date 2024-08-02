import pygame as pg
import time
import numpy as np

bg_color = (10, 10, 10)
grid_color = (40, 40, 40)
die_next = (170, 170, 170)
alive_next = (255, 255, 255)
size = 10

def update(screen, cells, size, with_progress=False, alive_color=alive_next):
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))

    for row, col in np.ndindex(cells.shape):
        alive = np.sum(cells[row-1:row+2, col-1:col+2]) - cells[row, col]
        color = bg_color if cells[row, col] == 0 else alive_color

        if cells[row, col] == 1:
            if alive < 2 or alive > 3:
                if with_progress:
                    color = die_next
            elif 2 <= alive <= 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = alive_color
        else:
            if alive == 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = alive_color

        pg.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))

    return updated_cells

def main():
    pg.init()
    cx, cy = (50, 50)
    screen = pg.display.set_mode((cx * size, cy * size))
    pg.display.set_caption("Game of Life")

    color = (0, 105, 28)

    cells = np.zeros((cy, cx))
    screen.fill(grid_color)
    update(screen, cells, size)
    pg.display.flip()

    running = False

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    running = not running
                    update(screen, cells, size, alive_color=color)
                    pg.display.update()
            if pg.mouse.get_pressed()[0]:
                x, y = pg.mouse.get_pos()
                cells[y // size, x // size] = 1
                update(screen, cells, size, alive_color=color)
                pg.display.update()

        screen.fill(grid_color)

        if running:
            cells = update(screen, cells, size, alive_color=color, with_progress=True)
            pg.display.update()

        time.sleep(0.001)

if __name__ == "__main__":
    main()
