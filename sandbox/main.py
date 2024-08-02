from numpy import zeros as nZeros
from random import randint
import pygame
import particles as prt
from os import system, name as oName

width, height = [300] * 2
Gwindow = pygame.display.set_mode((width, height))
size = 3
colors = {  "sand": [(194, 178, 128), (176, 160, 111), (204, 191, 153), (247, 220, 136)], 
            "water": [(46, 65, 240), (19, 37, 207)],
            "wood": [(54, 25, 8), (92, 41, 11), (92, 46, 11)],   

            "white" : (255, 255, 255),
            "black" : (8, 8, 8),
            "red" : (255, 0, 0),
            "green" : (55, 232, 35),
            "blue" : (66, 123, 255) }

screenColor = colors["black"]
particle = 1 #indicate the active particle
prt.setSize((width, height, size))

class SandBox:
    def __init__(self):
        self.grid = nZeros((width*2, height + size))
        self.position = []
        self.prtMuch = int(size / 2)

    def addElement(self, posX, posY, element:int):
        if 0 <= posX <= width and 0 <= posY <= height:
            match element:
                case -1:
                    if self.grid[posX, posY] != 0:
                        self.grid[posX, posY] = 0
                        positions_to_remove = []
                        for i in range(self.prtMuch):
                            for j in range(self.prtMuch):
                                # Collect positions that match the coordinates to remove later
                                positions_to_remove.append((posX-i, posY+j))
                                self.grid[posX-i, posY+j] = 0

                        # Remove matching positions without considering color and element
                        self.position = [pos for pos in self.position if (pos[0], pos[1]) not in positions_to_remove]

                case 1:
                    if self.grid[posX, posY] in (0, 2):
                        color = colors["sand"][randint(0, len(colors["sand"])-1)]
                        self.position.append((posX, posY, color, element))
                        for i in range(self.prtMuch):
                            for j in range(self.prtMuch):
                                self.position.append((posX-i, posY+j, color, element))
                                self.grid[posX-i, posY+j] = 1

                case 2:
                    if self.grid[posX, posY] == 0:
                        color = colors["water"][randint(0, len(colors["water"])-1)]
                        for i in range(self.prtMuch):
                            self.position.append((posX-i, posY, color, element))
                            self.grid[posX-i, posY] = 2

                case 3:
                    if self.grid[posX, posY] in (0, 2):
                        color = colors["wood"][randint(0, len(colors["wood"])-1)]
                        for i in range(self.prtMuch):
                            for j in range(self.prtMuch):
                                self.position.append((posX-i, posY+j, color, element))
                                self.grid[posX-i, posY+j] = 3
                case _:
                    raise SyntaxError

    def update_con(self):
        sand_positions = [pos for pos in self.position if pos[3] == 1]
        water_positions = [pos for pos in self.position if pos[3] == 2]
        others = [pos for pos in self.position if pos[3] == 3]

        self.position =  prt.water(water_positions, self.grid).update() + prt.sand(sand_positions, self.grid).update() + others

    def draw(self, win):
        for pos in self.position:
            pygame.draw.rect(win, pos[2], (pos[0],pos[1],size,size), 0)      

class Button:
    def __init__(self, x, y, width, height, imagePath, color, hover_color, callback, callback_arg):
        stroke = 4
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.active = False
        self.activeColor = colors["green"]
        self.callback = (callback, callback_arg) if callback_arg else callback
        self.hover_color = hover_color if hover_color else color
        image = pygame.image.load(imagePath)
        self.image = pygame.transform.scale(image, (width, height))
        self.stroke = pygame.Rect(x - stroke/2, y - stroke/2, width+stroke, height+stroke)

    def draw(self, screen, bgColor):
        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Check for mouse hover
        if self.active:
            current_color = self.activeColor
        elif self.rect.collidepoint(mouse_pos):
            current_color = self.hover_color
        else:
            current_color = self.color

        # Draw the button
        pygame.draw.rect(screen, current_color, self.stroke)
        pygame.draw.rect(screen, bgColor, self.rect)
        image_rect = self.image.get_rect(center=self.stroke.center)
        screen.blit(self.image, image_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if type(self.callback) == tuple: 
                    run_func = self.callback[0](self.callback[1])
                    if run_func: return False
                else: self.callback() 
                return True
        return False
    

def reset_buttons(buttons):
    for button in buttons:
        button.active = False

def set_particle(id:int):
    global particle

    particle = id

def clear(sandBox):
    sandBox.position = []
    sandBox.grid = nZeros((width*2, height + size))
    return True

def main():
    global particle

    runnin = True
    clock = pygame.time.Clock()
    
    sandBox = SandBox()

    sandButton = Button(20, 20, 24, 24, "assets/sand.png", colors["white"], colors["blue"], set_particle, 1)
    waterButton = Button(60, 20, 24, 24, "assets/water.png", colors["white"], colors["blue"], set_particle, 2)
    woodButton = Button(100, 20, 24, 24, "assets/wood.png", colors["white"], colors["blue"], set_particle, 3)
    eraseButton = Button(140, 20, 24, 24, "assets/eraser.png", colors["white"], colors["blue"], set_particle, -1)
    clearButton = Button(180, 20, 24, 24, "assets/paper.png", colors["white"], colors["red"], clear, sandBox)

    buttons = [sandButton, waterButton, woodButton, eraseButton, clearButton]
    
    while runnin:
        clock.tick(100) #To play with the speed 
        pygame.display.set_caption("sandBox - FPS: {}".format(int(clock.get_fps())))
        Gwindow.fill(screenColor)

        for button in buttons:
            button.draw(Gwindow, screenColor)
        
        for event in pygame.event.get():

            if event.type== pygame.QUIT:
                runnin= False
                system("rmdir /S /Q __pycache__" if oName == "nt" else 'rm -rf __pycache__')
                #clear cache

            elif pygame.mouse.get_pressed()[0]:
                pos=pygame.mouse.get_pos()
                if pos[1] >= 50: sandBox.addElement(pos[0]-pos[0]%size,pos[1]-pos[1]%size, particle)


            elif event.type == pygame.KEYUP:
                match event.key:  
                    case pygame.K_a: 
                        sandBox.position = []
                        sandBox.grid = nZeros((width*2, height + size))

            for button in buttons:
                if button.is_clicked(event):
                    reset_buttons(buttons)
                    button.active = True
                    

            
        
        sandBox.draw(Gwindow)
        sandBox.update_con()
        
                
        pygame.display.update()
    pygame.quit()
    
pygame.init()
main()