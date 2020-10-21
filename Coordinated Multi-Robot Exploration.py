#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import random
import pygame as pg
from scipy.spatial import distance
pg.init()

width = 800
height = 600
nSquares = 20

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)
purple = (166, 0, 255)
teal = (0, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 255)
orange = (255, 127, 0)
grey = (66, 66, 66)

colors = [yellow, purple, red, teal, green, blue, orange]

arrow = pg.image.load('arrow.png')
#arrow = pg.transform.scale(arrow, ())

gameDisplay = pg.display.set_mode((width, height))

clock = pg.time.Clock()

# fix self.margin

#class Square:
#    def __init__(self):
#        self.color
#        
#    def set_color(color):
#        this.color = color
#        
#    def display_square()

#def hill_climb_search():
        
class Empty():
    def __init__(self):
        self.color = white
        self.type = "empty"
        
    def display(self, square):
        pg.draw.rect(gameDisplay, self.color, square)
        
    def get_type(self):
        return self.type
    
class Wall():
    def __init__(self):
        self.color = grey
        self.type = "wall"
        
    def display(self, square):
        pg.draw.rect(gameDisplay, self.color, square)
        
    def get_type(self):
        return self.type
        
class Visited():
    def __init__(self, color):
        self.color = color
        self.type = "visited"
        
    def get_type(self):
        return self.type
    
    def display(self, square):
        pg.draw.rect(gameDisplay, self.color, square)
        

class Bot():
    def __init__(self, number, margin, position):
        self.margin = margin
        self.x = position[0]
        self.y = position[1]
        self.position = position
        self.number = number
        self.color = self.set_color(number)
        self.type = "bot"
        self.direction = 270
        self.arrow = pg.transform.scale(arrow, (margin, margin))
        self.arrow = pg.transform.rotate(self.arrow, 90)
        self.actions = {"left": False, "right": True, "up": False, "down": True}
        
    def set_color(self, number):
        return colors[number]
    
    def get_color(self):
        return self.color
    
    def get_actions(self):
        return self.actions
    
    def get_arrow(self):
        return self.arrow
    
    def get_type(self):
        return self.type
    
    def get_number(self):
        return self.number
    
    def get_position(self):
        return self.position
    
    def set_actions(self, actions):
        self.actions = actions
        
    def set_position(self, position):
        self.x = position[0]
        self.y = position[1]
    
    def set_direction(self, newAngle):
        self.arrow = pg.transform.rotate(self.arrow, newAngle - self.direction)
        self.direction = newAngle
        
    def display(self, square):
        pg.draw.rect(gameDisplay, self.color, square)
        gameDisplay.blit(self.arrow, (self.margin * self.x + 1, self.margin * self.y + 1))
        
        
class Grid:
    
    def __init__(self, width, height, nSquares, factor):
        self.width = width
        self.height = height
        self.nSquares = nSquares
        self.factor = factor
        self.squares = [[Empty() for y in range(int(height / (width / nSquares)))] for x in range(nSquares)]
        
        for x in range(len(self.squares)):
            self.squares[x][0] = Wall()
            self.squares[x][len(self.squares[0]) - 1] = Wall()
            
        for y in range(len(self.squares[0])):
            self.squares[0][y] = Wall()
            self.squares[len(self.squares) - 1][y] = Wall()
            
        self.place_walls()
        self.botLocations = []    
        self.margin = int(self.width / nSquares)    
        #self.arrowPosition = (1, 1) 
        self.botCount = 0
        self.squares[1][1] = Bot(self.botCount, self.margin, (1, 1))
        self.botLocations.append((1, 1))
        self.botCount += 1
        self.goal = (18, 6)
        
        #self.arrow = pg.transform.scale(arrow, (self.margin, self.margin))
        #self.arrow = pg.transform.rotate(self.arrow, 90)
        #self.actions = {"left": False, "right": True, "up": False, "down": True}
        
    def place_walls(self):    
        for x in range(1, len(self.squares) - 1):
            for y in range(1, len(self.squares[0]) - 1):
                if random.randint(1, self.factor) == 1:
                    self.squares[x][y] = Wall()
                
                
    def create_rect(self, x, y):
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
                square = self.create_rect(x, y)
                self.squares[x][y].display(square)
                

                #if(self.squares[x][y] == "empty"):
                #    pass
                    #square = self.create_rect(x, y)
                    #pg.draw.rect(gameDisplay, yellow, square)
                    #gameDisplay.blit(self.arrow, (self.margin * x + 1, self.margin * y + 1))
                #elif(self.squares[x][y] == "wall"):
                #    square = self.create_rect(x, y)
                #    pg.draw.rect(gameDisplay, grey, square)
                #elif(self.squares[x][y] == "visited"):
                #    square = self.create_rect(x, y)
                #    pg.draw.rect(gameDisplay, yellow, square)
                #else:  #if(self.squares[x][y] == "bot"):
                #    square = self.create_rect(x, y)
                #    pg.draw.rect(gameDisplay, yellow, square)
                #    gameDisplay.blit(self.squares[x][y].get_arrow(), (self.margin * x + 1, self.margin * y + 1))
                
    def set_wall(self, coordinates):
        x = int(coordinates[0] / self.margin)
        y = int(coordinates[1] / self.margin)
        
        if self.squares[x][y].get_type() == "empty":
            self.squares[x][y] = Wall()
        elif self.squares[x][y].get_type() == "wall":
            self.squares[x][y] = Empty() 
            
    def set_bot(self, coordinates):

        x = int(coordinates[0] / self.margin)
        y = int(coordinates[1] / self.margin)
        
        if self.squares[x][y].get_type() == "empty" or self.squares[x][y].get_type() == "wall":
            self.squares[x][y] = Bot(self.botCount, self.margin, (x, y))
            self.botLocations.append(self.squares[x][y].get_position())
            self.botCount += 1        
            
    #def rotate_arrow(self, newAngle):
    #    self.arrow = pg.transform.rotate(self.arrow, newAngle - self.arrowDirection)
    #    self.arrowDirection = newAngle
    
    def get_bot_position(number):
        for x in range(len(self.squares)):
            for y in range(len(self.squares[0])):
                if self.squares[x][y].get_type() == "bot":
                    if self.squares[x][y].get_number() == number:
                        return (x, y)
                
        
    def move_bot(self, direction, number):
        
        position = self.botLocations[number]
        
        x = position[0]
        y = position[1]
        
        actions = self.squares[x][y].get_actions()
        
        if actions[direction]:
            
            tempBot = self.squares[x][y]
            
            self.squares[x][y] = Visited(tempBot.get_color())
            
            if direction == "left":
                tempBot.set_direction(90)
                self.squares[x - 1][y] = tempBot
                self.squares[x - 1][y].set_position((x - 1, y))
                self.botLocations[number] = (x - 1, y)
                self.update_actions((x - 1, y))
                
            elif direction == "right":
                tempBot.set_direction(270)
                self.squares[x + 1][y] = tempBot
                self.squares[x + 1][y].set_position((x + 1, y))
                self.botLocations[number] = (x + 1, y)
                self.update_actions((x + 1, y))
                
            elif direction == "up":
                tempBot.set_direction(0)
                self.squares[x][y - 1] = tempBot
                self.squares[x][y - 1].set_position((x, y - 1))
                self.botLocations[number] = (x, y - 1)
                self.update_actions((x, y - 1))

            elif direction == "down":
                tempBot.set_direction(180)
                self.squares[x][y + 1] = tempBot
                self.squares[x][y + 1].set_position((x, y + 1))
                self.botLocations[number] = (x, y + 1)
                self.update_actions((x, y + 1))
                
        #self.update_actions((x, y))
                           
            
    def update_actions(self, position):
        x = position[0]
        y = position[1]
        
        actions = {"left": False, "right": False, "up": False, "down": False}
        
        if self.squares[x - 1][y].get_type() not in ["wall", "bot"]:
            actions["left"] = True
        else:
            actions["left"] = False 

        if self.squares[x + 1][y].get_type() not in ["wall", "bot"]:
            actions["right"] = True
        else:
            actions["right"] = False
            
        if self.squares[x][y - 1].get_type() not in ["wall", "bot"]:
            actions["up"] = True
        else:
            actions["up"] = False    
          
        #print(x, y)
        if self.squares[x][y + 1].get_type() not in ["wall", "bot"]:
            actions["down"] = True
        else:
            actions["down"] = False
            
        self.squares[x][y].set_actions(actions)
        
    def get_best_action(self, position):
        x = position[0]
        y = position[1]
        print(position)
        actions = self.squares[x][y].get_actions()
        print(actions)
        
        possibleActions = {"left": 1000000, "right": 1000000, "up": 1000000, "down": 1000000}
        
        if actions["left"]:
            #possibleActions.append({"left": distance.euclidean((x - 1, y), self.goal)})
            possibleActions["left"] = distance.euclidean((x - 1, y), self.goal)
            
        if actions["right"]:
            #possibleActions.append({"right": distance.euclidean((x + 1, y), self.goal)})
            possibleActions["right"] = distance.euclidean((x + 1, y), self.goal)
            
        if actions["up"]:
            #possibleActions.append({"up": distance.euclidean((x, y - 1), self.goal)})
            possibleActions["up"] = distance.euclidean((x, y - 1), self.goal)
            
        if actions["down"]:
            #possibleActions.append({"down": distance.euclidean((x, y + 1), self.goal)})
            possibleActions["down"] = distance.euclidean((x, y + 1), self.goal)
            
        keys = list(possibleActions.keys())
        values = list(possibleActions.values())
        #print(possibleActions)
        #print(keys)
        #print(values)
        
        #print(keys[values.index(min(values))])
            
        return keys[values.index(min(values))]
    
factor = 4
            
grid = Grid(width, height, nSquares, factor)

pg.display.set_caption('Coordinated Multi-Robot Exploration')

pg.display.update()

#print(grid.actions)

gameExit = False
startSearching = False

while not gameExit:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            gameExit = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                startSearching = True
                #grid.move_bot("right", 0)
                #grid.move_bot("right", 1)
        #    grid.update_actions()
        #    if event.key == pg.K_LEFT:
        #        grid.rotate_arrow(90)
        #        grid.move_arrow("left")
        #    if event.key == pg.K_RIGHT:
        #        grid.rotate_arrow(270)
        #        grid.move_arrow("right")
        #    elif event.key == pg.K_UP:
        #        grid.rotate_arrow(0)
        #        grid.move_arrow("up")
        #    elif event.key == pg.K_DOWN:
        #        grid.rotate_arrow(180)
        #        grid.move_arrow("down")
        elif pg.mouse.get_pressed()[0]:
            grid.set_wall(pg.mouse.get_pos())
        elif pg.mouse.get_pressed()[2]:
            grid.set_bot(pg.mouse.get_pos())
        
        # right mouse click -> add bot
            
    gameDisplay.fill(white)
    
    if startSearching:
    
        botNum = 0
        for botPosition in grid.botLocations:
            #print(botPosition)
            x = botPosition[0]
            y = botPosition[1]
            
            grid.update_actions(botPosition)
            
            tempBot = grid.squares[x][y]
            
            directionToMove = grid.get_best_action(botPosition)
            grid.move_bot(directionToMove, botNum)

            botNum += 1
            
        time.sleep(0.5)
                
        

    grid.display()
    
    pg.display.update()
    
    #time.sleep(0.5)
    
    
pg.quit()
quit()


# In[3]:


import random
print(random.randint(1, 2))


# In[ ]:





# In[ ]:




