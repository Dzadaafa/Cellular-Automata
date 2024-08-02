import numpy as np
from random import randint
from os import name as osName, system
from time import sleep

width, height = 20, 20
size = 1

class Grid:
    def __init__(self):
        self.grid = np.zeros((height, width + size))
        self.position = []

    def addSand(self, posY, posX):
        if 0 <= posX <= width and 0 <= posY <= height:
            if self.grid[posY, posX] == 0:
                self.grid[posY, posX] = 1
                self.position.append((posY, posX))

    def pos_update(self):
        new_positions = []
        for pos in self.position:
            listedPos = list(pos)
            if pos[0] >= height - size:
                new_positions.append(pos)
            elif self.grid[pos[0] + size, pos[1]] == 0:
                self.grid[pos[0], pos[1]] = 0
                self.grid[pos[0] + size, pos[1]] = 1
                listedPos[0] += size
                new_positions.append(tuple(listedPos))
            else:
                if pos[1] > 0 and self.grid[pos[0] + size, pos[1] - size] == 0:
                    self.grid[pos[0], pos[1]] = 0
                    self.grid[pos[0] + size, pos[1] - size] = 1
                    listedPos[0] += size
                    listedPos[1] -= size
                    new_positions.append(tuple(listedPos))
                elif pos[1] < width and self.grid[pos[0] + size, pos[1] + size] == 0:
                    self.grid[pos[0], pos[1]] = 0
                    self.grid[pos[0] + size, pos[1] + size] = 1
                    listedPos[0] += size
                    listedPos[1] += size
                    new_positions.append(tuple(listedPos))
                else:
                    new_positions.append(pos)

        self.position = new_positions

    def draw(self):
        system("cls" if osName == "nt" else "clear")
        for y in self.grid:
            for x in y:
                print("*" if x > 0 else " ", end=" ")
            print()

def main():
    sand = Grid()
    randomkah = 0

    while True:
        if randomkah > 4:
            sand.addSand(randint(0, 9), randint(9, 12))
            sand.addSand(randint(0, 9), randint(9, 12))
            sand.addSand(randint(0, 9), randint(9, 12))
            randomkah = 0

        sand.pos_update()
        sand.draw()

        randomkah += 1
        sleep(0.05)  # Reduced sleep time for smoother animation

main()