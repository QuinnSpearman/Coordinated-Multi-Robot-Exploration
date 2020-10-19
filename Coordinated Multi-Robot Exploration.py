#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pygame as pg
pg.init()

width = 800
height = 600
nSquares = 20

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)
grey = (66, 66, 66)

arrow = pg.image.load('arrow.png')
#arrow = pg.transform.scale(arrow, ())

gameDisplay = pg.display.set_mode((width, height))

# fix self.margin

class Grid:
    
    def __init__(self, width, height, nSquares):
        self.width = width
        self.height = height
        self.nSquares = nSquares
        self.squares = [["empty" for y in range(int(height / (width / nSquares)))] for x in range(nSquares)]
        
        for x in range(len(self.squares)):
            self.squares[x][0] = "wall"
            self.squares[x][len(self.squares[0]) - 1] = "wall"
            
        for y in range(len(self.squares[0])):
            self.squares[0][y] = "wall"
            self.squares[len(self.squares) - 1][y] = "wall"
            
        self.arrowPosition = (1, 1)    
        self.squares[self.arrowPosition[0]][self.arrowPosition[1]] = "bot"
        self.arrowDirection = 270
        self.margin = int(self.width / nSquares)
        self.arrow = pg.transform.scale(arrow, (self.margin, self.margin))
        self.arrow = pg.transform.rotate(self.arrow, 90)
        self.actions = {"left": False, "right": True, "up": False, "down": True}
        
    def create_rect(self, x, y):po
        w = (x * self.margin) + 2
        h = (y * self.margin) + 2
        return [w, h, self.margin - 2, self.margin - 2]
        
    def display(self):
        for i in range(nSquares + 1):
            pg.draw.line(gameDisplay, black, (self.margin * i, 0), (self.margin * i, height), 2)
        pg.draw.line(gameDisplay, black, (width - 2, 0), (width - 2, height), 2)

        for i in range(int(height / self.margin)):
            pg.draw.line(gameDisplay, black, (0, self.margin * i), (width, self.margin * i), 2)
        pg.draw.line(gameDisplay, black, (0, height - 2), (width, height - 2), 2)
        
        for x in range(nSquares):
            for y in range(int(height / (width / nSquares))):
                if(self.squares[x][y] == "bot"):
                    square = self.create_rect(x, y)
                    pg.draw.rect(gameDisplay, yellow, square)
                    gameDisplay.blit(self.arrow, (self.margin * x + 1, self.margin * y + 1))
                elif(self.squares[x][y] == "wall"):
                    square = self.create_rect(x, y)
                    pg.draw.rect(gameDisplay, grey, square)
                elif(self.squares[x][y] == "visited"):
                    square = self.create_rect(x, y)
                    pg.draw.rect(gameDisplay, yellow, square)
                
    def set_wall(self, coordinates):
        x = int(coordinates[0] / 40)
        y = int(coordinates[1] / 40)
        
        if self.squares[x][y] == "empty":
            self.squares[x][y] = "wall"
        elif self.squares[x][y] == "wall":
            self.squares[x][y] = "empty"
        
    def rotate_arrow(self, newAngle):
        self.arrow = pg.transform.rotate(self.arrow, newAngle - self.arrowDirection)
        self.arrowDirection = newAngle
        
    def move_arrow(self, direction):
        if self.actions[direction]:
            
            self.squares[self.arrowPosition[0]][self.arrowPosition[1]] = "visited"
            
            if direction == "left":
                self.squares[self.arrowPosition[0] - 1][self.arrowPosition[1]] = "bot"
                self.arrowPosition = (self.arrowPosition[0] - 1, self.arrowPosition[1])
            elif direction == "right":
                self.squares[self.arrowPosition[0] + 1][self.arrowPosition[1]] = "bot"
                self.arrowPosition = (self.arrowPosition[0] + 1, self.arrowPosition[1])
            elif direction == "up":
                self.squares[self.arrowPosition[0]][self.arrowPosition[1] - 1] = "bot"
                self.arrowPosition = (self.arrowPosition[0], self.arrowPosition[1] - 1)
            elif direction == "down":
                self.squares[self.arrowPosition[0]][self.arrowPosition[1] + 1] = "bot"
                self.arrowPosition = (self.arrowPosition[0], self.arrowPosition[1] + 1)
                
            
    def update_actions(self):
        x = self.arrowPosition[0]
        y = self.arrowPosition[1]
        

        if self.squares[x - 1][y] != "wall":
            self.actions["left"] = True
        else:
            self.actions["left"] = False 

        if self.squares[x + 1][y] != "wall":
            self.actions["right"] = True
        else:
            self.actions["right"] = False
            
        if self.squares[x][y - 1] != "wall":
            self.actions["up"] = True
        else:
            self.actions["up"] = False    
          
        if self.squares[x][y + 1] != "wall":
            self.actions["down"] = True
        else:
            self.actions["down"] = False
            
grid = Grid(width, height, nSquares)

pg.display.set_caption('Coordinated Multi-Robot Exploration')

pg.display.update()

print(grid.actions)

gameExit = False

while not gameExit:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            gameExit = True
        if event.type == pg.KEYDOWN:
            grid.update_actions()
            if event.key == pg.K_LEFT:
                grid.rotate_arrow(90)
                grid.move_arrow("left")
            if event.key == pg.K_RIGHT:
                grid.rotate_arrow(270)
                grid.move_arrow("right")
            elif event.key == pg.K_UP:
                grid.rotate_arrow(0)
                grid.move_arrow("up")
            elif event.key == pg.K_DOWN:
                grid.rotate_arrow(180)
                grid.move_arrow("down")
        elif event.type == pg.MOUSEBUTTONUP:
            grid.set_wall(pg.mouse.get_pos())
            
    gameDisplay.fill(white)

    grid.display()
    
    pg.display.update()
    
pg.quit()
quit()


# In[ ]:




