#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import random
import pygame as pg
from scipy.spatial import distance
pg.init()

width = 700
height = 700
nSquares = 50

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

gameDisplay = pg.display.set_mode((width, height))

clock = pg.time.Clock()
        
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
        
class Bot_Exploration():
    pass
        
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
        self.V = []
        self.targetPoint = None
        self.visitedThisSearch = []
        
    def initialize_visited(self):
        self.visitedThisSearch = []
    
    def add_to_visited(self, coordinates):
        self.visitedThisSearch.append(coordinates)
        
    def cell_visited_frequency(self, coordinates):
        freq = 0
        for i in self.visitedThisSearch:
            if i == coordinates:
                freq += 1
        return freq
        
    def set_V(self, V):
        self.V = V
        
    def get_V(self):
        return self.V
        
    def set_target_point(self, targetPoint):
        self.targetPoint = targetPoint
        
    def get_target_point(self):
        return self.targetPoint
        
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
    
    def get_direction(self):
        return self.direction
    
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
    
    def __init__(self, width, height, nSquares, percentage, obstacleType):
        self.vision = 1
        self.width = width
        self.height = height
        self.nSquares = nSquares
        self.percentage = percentage
        self.squares = [[Empty() for y in range(int(height / (width / nSquares)))] for x in range(nSquares)]
        self.frontierCellsList = []
        
        for x in range(len(self.squares)):
            self.squares[x][0] = Wall()
            self.squares[x][len(self.squares[0]) - 1] = Wall()
            
        for y in range(len(self.squares[0])):
            self.squares[0][y] = Wall()
            self.squares[len(self.squares) - 1][y] = Wall()
        
        if obstacleType == 1:
            self.place_walls()
        else:
            self.place_large_obstacles()
            
        self.botLocations = []    
        self.margin = int(self.width / nSquares)    
        self.botCount = 0
        self.squares[1][1] = Bot(self.botCount, self.margin, (1, 1))
        self.botLocations.append((1, 1))
        self.set_visited(self.botCount)
        self.botCount += 1
        self.goal = (18, 6)
        self.frontierCellsDict = {}

    
    def get_bots_with_target_points():
        
        index = 0
        for coordinates in self.botLocations:
            x = coordinates[0]
            y = coordinates[1]
            
            if self.squares[x][y].get_target_point() == None:
                botsWithTargetPoints
                
                
    def costs(botX, botY):
        costs = []
        
        minDistance = 1000
        
        for coordinates in self.frontierCells:
            targetX = coordinates[0]
            targetY = coordinates[1]
            
            tempDistance = distance.euclidean((botX, botY), coordinates)
            #tempDistance = distance.euclidean((botX, botY), coordinates)
            
            
            if tempDistance < minDistance:
                minDistance = tempDistance
                closest = coordinates
                
        return closest
    
    def distance(self, start, end):
        startX = start[0]
        startY = start[1]
        endX = end[0]
        endY = end[1]
        
        return abs(startX - endX) + abs(startY - endY)
    
    def V(self, botX, botY):
 
        V = []
        
        closestDistance = 1000   
        
        for frontierCell in self.frontierCellsDict:
            
            V.append({"coordinates": frontierCell, "distance": distance.euclidean((botX, botY), frontierCell)})
   
            
        return V
        
                
       
        
    def find_closest_neighbor(self, frontierCell, botPosition):
        x = frontierCell[0]
        y = frontierCell[1]
        
        
        initialX = x - self.vision
        initialY = y - self.vision
        
        minDistance= 1000
        minUnknown = 0
        
        for i in range(3):
            for j in range(3):
                
                if (initialX + i, initialY + j) == frontierCell or self.squares[initialX + i][initialY + j].get_type() in ["wall", "bot", "visited"]:
                    continue
                    
                if (initialX + i, initialY + j) not in self.frontierCellsDict:
                    tempDistance = distance.euclidean((initialX + i, initialY + j), botPosition)
                    if tempDistance < minDistance:
                        minDistance = tempDistance
                        minUnknown = (initialX + i, initialY + j)
                        
        return minUnknown

    def place_walls(self):    
        sumOfObstacles = 0
        waitingObstacles = 0
        #random.seed(1)
        
        for x in range(1, len(self.squares) - 1):
            for y in range(1, len(self.squares[0]) - 1):
                wallsInProximity = 0
                initialX = x - self.vision
                initialY = y - self.vision
                for i in range(3):
                    for j in range(3):
                        if self.squares[initialX + i][initialY + j].get_type() == "wall":
                            wallsInProximity += 1
                
                #if wallsInProximity <= 0:
                if random.randint(1, 100) <= percentage:
                    self.squares[x][y] = Wall()
                    sumOfObstacles += 1
                        
        
        
    def place_large_obstacles(self):
        #random.seed(0)
        for x in range(2, len(self.squares) - 2):
            for y in range(2, len(self.squares[0]) - 2):
                wallInProximity = False
                initialX = x - self.vision
                initialY = y - self.vision
                for i in range(4):
                    for j in range(4):
                        if self.squares[initialX + i][initialY + j].get_type() == "wall":
                            wallInProximity = True
                            
                if random.randint(1, 100) <= percentage and not wallInProximity:
                    for i in range(2):
                        for j in range(2):
                            self.squares[x + i][y + j] = Wall()
                    
                
        
                                            
                
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

                
    def set_wall(self, coordinates):
        x = int(coordinates[0] / self.margin)
        y = int(coordinates[1] / self.margin)
        
        if self.squares[x][y].get_type() == "empty":
            self.squares[x][y] = Wall()
        elif self.squares[x][y].get_type() == "wall":
            self.squares[x][y] = Empty() 
        else:
            pass
            
    def set_bot(self, coordinates):

        x = int(coordinates[0] / self.margin)
        y = int(coordinates[1] / self.margin)
        
        if self.squares[x][y].get_type() == "empty" or self.squares[x][y].get_type() == "wall":
            self.squares[x][y] = Bot(self.botCount, self.margin, (x, y))
            self.botLocations.append(self.squares[x][y].get_position())
            self.set_visited(self.botCount)
            self.botCount += 1    
        else:
            pass
    
    def get_bot_position(self, number):
        return self.botLocations[number]
                    
    def get_frontier_cells(self):
        return self.frontierCellsDict
    
    def set_visited(self, botNumber):
        
        botCoordinates = self.botLocations[botNumber]
        x = botCoordinates[0]
        y = botCoordinates[1]
        
        #initialX = x - self.vision
        #initialY = y - self.vision  
        
        if self.squares[x + 1][y].get_type() not in ["visited", "wall", "bot"]:
            self.squares[x + 1][y] = Visited(colors[botNumber])
        
        if self.squares[x - 1][y].get_type() not in ["visited", "wall", "bot"]:
            self.squares[x - 1][y] = Visited(colors[botNumber])
        
        if self.squares[x][y + 1].get_type() not in ["visited", "wall", "bot"]:
            self.squares[x][y + 1] = Visited(colors[botNumber])
        
        if self.squares[x][y - 1].get_type() not in ["visited", "wall", "bot"]:
            self.squares[x][y - 1] = Visited(colors[botNumber])
        
        if self.squares[x + 1][y + 1].get_type() not in ["visited", "wall", "bot"]:
            #if self.squares[x + 1][y].get_type() is not "wall" and self.squares[x][y + 1].get_type() is not "wall":
            self.squares[x + 1][y + 1] = Visited(colors[botNumber])
        
        if self.squares[x + 1][y - 1].get_type() not in ["visited", "wall", "bot"]:
            #if self.squares[x][y - 1].get_type() is not "wall" and self.squares[x + 1][y].get_type() is not "wall":
            self.squares[x + 1][y - 1] = Visited(colors[botNumber])
        
        if self.squares[x - 1][y + 1].get_type() not in ["visited", "wall", "bot"]:
            #if self.squares[x - 1][y].get_type() is not "wall" and self.squares[x][y + 1].get_type() is not "wall":
            self.squares[x - 1][y + 1] = Visited(colors[botNumber])
        
        if self.squares[x - 1][y - 1].get_type() not in ["visited", "wall", "bot"]:
            #if self.squares[x - 1][y].get_type() is not "wall" and self.squares[x][y - 1].get_type() is not "wall":
            self.squares[x - 1][y - 1] = Visited(colors[botNumber])
        
        return False          
                        
    def check_if_frontier_cell(self, x, y):
        
        if self.squares[x + 1][y].get_type() not in ["visited", "wall", "bot"]:
            return True
        
        if self.squares[x - 1][y].get_type() not in ["visited", "wall", "bot"]:
            return True
        
        if self.squares[x][y + 1].get_type() not in ["visited", "wall", "bot"]:
            return True
        
        if self.squares[x][y - 1].get_type() not in ["visited", "wall", "bot"]:
            return True
        
        if self.squares[x + 1][y + 1].get_type() not in ["visited", "wall", "bot"]:
        #    if self.squares[x + 1][y].get_type() is not "wall" and self.squares[x][y + 1].get_type() is not "wall":
            return True
        
        if self.squares[x + 1][y - 1].get_type() not in ["visited", "wall", "bot"]:
        #    if self.squares[x][y - 1].get_type() is not "wall" and self.squares[x + 1][y].get_type() is not "wall":
            return True
        
        if self.squares[x - 1][y + 1].get_type() not in ["visited", "wall", "bot"]:
        #    if self.squares[x - 1][y].get_type() is not "wall" and self.squares[x][y + 1].get_type() is not "wall":
            return True
        
        if self.squares[x - 1][y - 1].get_type() not in ["visited", "wall", "bot"]:
        #    if self.squares[x - 1][y].get_type() is not "wall" and self.squares[x][y - 1].get_type() is not "wall":
            return True
        
        return False       
            
    def set_frontier_cells(self):
        
        self.frontierCellsList = []
        
        for x in range(len(self.squares)):
            for y in range(len(self.squares[0])):
                if self.squares[x][y].get_type() == "visited":
                    if self.check_if_frontier_cell(x, y):
                        
                        self.frontierCellsList.append((x,y))
                        
        self.frontierCellsDict = {i: 1 for i in self.frontierCellsList}                
                        
    def target_point_in_vision(self, botPosition, targetPoint):
        
        x = botPosition[0]
        y = botPosition[1]
        
        initialX = x - self.vision
        initialY = y - self.vision
        
        for i in range(3):
            for j in range(3):
                if targetPoint == (initialX + i, initialY + j):
                    return True
                
        return False
                    

    def adjust_utility(self, targetPoint):
        
        for frontierCell in self.frontierCellsList:
            d = distance.euclidean(targetPoint, frontierCell)
            if d < 2:
                p = 1 - (d / 2)
            else:
                p = 0

            self.frontierCellsDict[frontierCell] -= p

    def move_bot(self, direction, number):
        
        # gets position of a bot based on its number
        position = self.botLocations[number]
        
        # x and y coordinates of the robot
        x = position[0]
        y = position[1]
                
        self.squares[x][y].add_to_visited(position)
        
        # retrieves possible actions of the bot at its current position    
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
                
        self.set_visited(number)
            
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

        if self.squares[x][y + 1].get_type() not in ["wall", "bot"]:
            actions["down"] = True
        else:
            actions["down"] = False
            
        self.squares[x][y].set_actions(actions)
        
    def get_best_action(self, position, targetPoint):
        x = position[0]
        y = position[1]

        actions = self.squares[x][y].get_actions()
        
        possibleActions = {"left": 1000000000000, "right": 1000000000000, "up": 1000000000000, "down": 1000000000000}
        
        if actions["left"]:
            possibleActions["left"] = distance.euclidean((x - 1, y), targetPoint)

            leftVisitedFrequency = self.squares[x][y].cell_visited_frequency((x - 1, y))

            if leftVisitedFrequency != 0:
                possibleActions["left"] *= leftVisitedFrequency**10
            
        if actions["right"]:
            possibleActions["right"] = distance.euclidean((x + 1, y), targetPoint)

            rightVisitedFrequency = self.squares[x][y].cell_visited_frequency((x + 1, y))

            if rightVisitedFrequency != 0:
                possibleActions["right"] *= rightVisitedFrequency**10

    
        if actions["up"]:
            possibleActions["up"] = distance.euclidean((x, y - 1), targetPoint)

            upVisitedFrequency = self.squares[x][y].cell_visited_frequency((x, y - 1))

            if upVisitedFrequency != 0:
                possibleActions["up"] *= upVisitedFrequency**10

            
        if actions["down"]:
            possibleActions["down"] = distance.euclidean((x, y + 1), targetPoint)

            downVisitedFrequency = self.squares[x][y].cell_visited_frequency((x, y + 1))

            if downVisitedFrequency != 0:
                possibleActions["down"] *= downVisitedFrequency**10
            
        #print(possibleActions)
        
            
        keys = list(possibleActions.keys())
        values = list(possibleActions.values())
        
        
            
        
        minDirection = keys[values.index(min(values))]
        #if not actions[minDirection]:
        #    if minDirection is "right":
                
        #        return self.get_new_action("right", "left", "up", "down", actions)
                
        #    elif minDirection is "left":
                
        #        return self.get_new_action("left", "right", "down", "up", actions)
                
        #    elif minDirection is "up":
                
        #        return self.get_new_action("up", "down", "left", "right", actions)
                
        #    elif minDirection is "down":
                
        #        return self.get_new_action("down", "up", "right", "left", actions)
        #else:
        return minDirection
    
    def get_new_action(self, f, b, l, r, actions):
        
        newDirVal = random.randint(1,2)

        if not actions[l] and not actions[r]:
            newDirVal = 3
        elif not actions[l]:
            newDirVal = 1
        elif not actions[r]:
            newDirVal = 2

        if newDirVal is 1: 
            minDirection = r
        elif newDirVal is 2: 
            minDirection = l
        elif newDirVal is 3:
            minDirection = b
        
        return minDirection
        
obstacleType = int(input("Enter an obstacle type |(1) small (2) large|: "))
percentage = int(input("Enter an obstacle percentage: "))
print("+ Left-click to place walls")
print("+ Right-click to place bots")
print("+ Press space-bar to start exploration")

grid = Grid(width, height, nSquares, percentage, obstacleType)

pg.display.set_caption('Coordinated Multi-Robot Exploration')

pg.display.update()

gameExit = False
startSearching = False
timerNotStarted = True

while not gameExit:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            gameExit = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                startSearching = True
        elif pg.mouse.get_pressed()[0]:
            grid.set_wall(pg.mouse.get_pos())
        elif pg.mouse.get_pressed()[2]:
            grid.set_bot(pg.mouse.get_pos())
            
    
            
    gameDisplay.fill(white)
    
    if startSearching:
        if timerNotStarted:
            startTime = time.time_ns()
            timerNotStarted = False
            
        
        botsWithoutTargetPoints = []
        

        grid.set_frontier_cells()

        frontierCells = grid.get_frontier_cells()
        #print(len(frontierCells))
        
        if len(grid.get_frontier_cells()) is 0:
            startSearching = False
            
        
        # Compute the cost for each robot of reaching each frontier cell
        for botPosition in grid.botLocations:
            
            botX = botPosition[0]
            botY = botPosition[1]
            
            tempV = grid.V(botX, botY)

            
            grid.squares[botX][botY].set_V(tempV) 
            
            if grid.squares[botX][botY].get_target_point() == None:
                botsWithoutTargetPoints.append((botX, botY))
            
        
            
        # while there is a robot left without a target point
        while len(botsWithoutTargetPoints) > 0:
            
            maxUtilityValue = 0
            maxUtilityCoordinates = 0
            maxUtilityBotPosition = 0
            maxUtilityBotNumber = 0
            
            for botPosition in botsWithoutTargetPoints:
                
                botX = botPosition[0]
                botY = botPosition[1]
                
                tempV = grid.squares[botX][botY].get_V()

                
                for i in range(len(tempV)):
                
                    vCoordinates = tempV[i]["coordinates"]
                    vValue = tempV[i]["distance"]
                    
                    
                    U = grid.frontierCellsDict[vCoordinates]
                    
                    
                    utility = U - (0.01 * vValue)
 
                    
                    if utility > maxUtilityValue:
                        maxUtilityValue = utility
                        maxUtilityCoordinates = vCoordinates
                        maxUtilityBotPosition = botPosition
                        maxUtilityBotNumber = grid.squares[botX][botY].get_number()
                        
            
            
            
            botsWithoutTargetPoints.remove(maxUtilityBotPosition)
            botX = maxUtilityBotPosition[0]
            botY = maxUtilityBotPosition[1]
            
            closestNeighbor = grid.find_closest_neighbor(maxUtilityCoordinates, maxUtilityBotPosition)

            
            grid.squares[botX][botY].set_target_point(closestNeighbor)

            grid.adjust_utility(closestNeighbor) 
            
            
            
        botNum = 0        
        
        for botPosition in grid.botLocations:

            x = botPosition[0]
            y = botPosition[1]
            
            grid.update_actions(botPosition)
            
            tempBot = grid.squares[x][y]
            #print(tempBot.get_target_point())
            directionToMove = grid.get_best_action(botPosition, grid.squares[x][y].get_target_point())
            grid.move_bot(directionToMove, botNum)
            
            botPosition = grid.get_bot_position(botNum)
            x = botPosition[0]
            y = botPosition[1]

            botNum += 1

            if grid.target_point_in_vision(botPosition, tempBot.get_target_point()):
                grid.squares[x][y].set_target_point(None)
                grid.squares[x][y].initialize_visited()
                
        grid.set_frontier_cells()
        if len(grid.get_frontier_cells()) is 0:
            startSearching = False
            endTime = time.time_ns()
            print("Runtime: " + str((endTime - startTime) / 1000000000) + "s")

        #time.sleep(0.02)

    grid.display()
    
    pg.display.update()
    
pg.quit()
quit()


# In[ ]:





# In[ ]:




