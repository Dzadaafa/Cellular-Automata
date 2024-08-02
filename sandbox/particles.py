from random import choice

width:int
height:int
size:int

def setSize(sizeAll:tuple) -> None:
    """
    tuple(width, height, size) in rows

    witdh of the screen
    height of the screen
    size of the pixel
    """

    global width, height, size

    width, height, size = sizeAll


class water:
    def __init__(self, positions, grid) -> None:
        self.grid = grid
        self.positions = positions

    def update(self) -> list:
        new_positions = []
        for pos in self.positions:
            listedPos = list(pos)
            if pos[1] >= height - size:
                new_positions.append(pos)
            elif self.grid[pos[0], pos[1] + size] == 0:
                self.grid[pos[0], pos[1]] = 0
                self.grid[pos[0], pos[1] + size] = 2
                listedPos[1] += size
                new_positions.append(tuple(listedPos))
            else:
                if pos[0] > 0 and self.grid[pos[0] - size, pos[1] + size] == 0 and self.grid[pos[0] - size, pos[1]] == 0:
                    self.grid[pos[0], pos[1]] = 0
                    self.grid[pos[0] - size, pos[1] + size] = 2
                    listedPos[0] -= size
                    listedPos[1] += size
                    new_positions.append(tuple(listedPos))
                elif pos[0] < width - size and self.grid[pos[0] + size, pos[1] + size] == 0 and self.grid[pos[0] + size, pos[1]] == 0:
                    self.grid[pos[0], pos[1]] = 0
                    self.grid[pos[0] + size, pos[1] + size] = 2
                    listedPos[0] += size
                    listedPos[1] += size
                    new_positions.append(tuple(listedPos))
                elif (pos[0] < width - size and pos[0] > 0) and (self.grid[pos[0] - size, pos[1]] == 0 and self.grid[pos[0] + size, pos[1]] == 0):
                    # Randomly decide whether to go left or right
                    if choice([True, False]):
                        self.grid[pos[0], pos[1]] = 0
                        self.grid[pos[0] - size, pos[1]] = 2
                        listedPos[0] -= size
                    else:
                        self.grid[pos[0], pos[1]] = 0
                        self.grid[pos[0] + size, pos[1]] = 2
                        listedPos[0] += size
                    new_positions.append(tuple(listedPos))
                elif pos[0] > 0 and self.grid[pos[0] - size, pos[1]] == 0:
                    self.grid[pos[0], pos[1]] = 0
                    self.grid[pos[0] - size, pos[1]] = 2
                    listedPos[0] -= size
                    new_positions.append(tuple(listedPos))
                elif pos[0] < width - size and self.grid[pos[0] + size, pos[1]] == 0:
                    self.grid[pos[0], pos[1]] = 0
                    self.grid[pos[0] + size, pos[1]] = 2
                    listedPos[0] += size
                    new_positions.append(tuple(listedPos))
                else:


                    new_positions.append(pos)

        return new_positions
    
class sand:
    def __init__(self, positions, grid) -> None:
        self.grid = grid
        self.position = positions
	
    def is_thru(self, x, y):
        return self.grid[x, y] in (0, 2)

    def ptc_bellow(self, x, y):
        return self.grid[x, y]

    def update(self) -> list:
        new_positions = []
        for pos in self.position:
            listedPos = list(pos)
            if pos[1] >= height - size:
                new_positions.append(pos)
            elif self.is_thru(pos[0], pos[1]+ size):
                self.grid[pos[0], pos[1]] = self.ptc_bellow(pos[0], pos[1]+ size)
                self.grid[pos[0], pos[1] + size] = 1
                listedPos[1] += size
                new_positions.append(tuple(listedPos))
            else:
                if pos[0] > 0 and self.is_thru(pos[0] - size, pos[1] + size) and self.is_thru(pos[0] - size, pos[1]):
                    self.grid[pos[0], pos[1]] = self.ptc_bellow(pos[0] - size, pos[1] + size)
                    self.grid[pos[0] - size, pos[1] + size] = 1
                    listedPos[0] -= size
                    listedPos[1] += size
                    new_positions.append(tuple(listedPos))
                elif pos[1] < width and self.is_thru(pos[0] + size, pos[1] + size) and self.is_thru(pos[0] + size, pos[1]):
                    self.grid[pos[0], pos[1]] = self.ptc_bellow(pos[0] + size, pos[1] + size)
                    self.grid[pos[0] + size, pos[1] + size] = 1
                    listedPos[0] += size
                    listedPos[1] += size
                    new_positions.append(tuple(listedPos))
                else:
                    new_positions.append(pos)

        return new_positions

class wood:
    def __init__(self, positions, grid) -> None:
        self.grid = grid
        self.position = positions

    def is_thru(self, x, y):
        return self.grid[x, y] in (0, 2)

    def update(self) -> list:
        new_positions = []
        for pos in self.position:
            listedPos = list(pos)
            if self.is_thru(pos[0], pos[1]):
                new_positions.append(pos)

        return new_positions
    


