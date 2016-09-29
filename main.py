"""
    
    First brains have only 2 hidden neuron and add news one rarely which originally have reasonably low weights (-0.5 to 0.5) so that it is more likely to be helpful


    How to add layers without massively altering network?

    Maybe add a layer before the one being duplicated of which has outputs equalling ~1 only to its corresponding neurons
    so that only small changes have been made, neurons also have very small weights connecting to each other neuron.
        
    More likely re create brain architecture entirely so that each neuron connects to whatever neurons it wants (not neurons behind itself though)
    and then there are no real 'layers' and more closely resmbles a brain.
    
    Another way to recreate brain is there are a set number of layers (maybe 5 because 5 layers is enough jeez) and neurons can connect to any
    neurons in future layers and add the that neurons sum so that when that neuron is reached to process is already has its sum.
    When new neuons are created they are given random layer with random connections to neurons in layers ahead of itself.


    What happens in real life with brain evolution and the addition of neurons?


    Try to comment more pls

"""

import pygame
import math
import random
import colours
import neural_net
import lines
import json
import funcs
pygame.init()
size = (1600, 900)  #(1280, 720)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Food Seeking Organisms")
gridSize = 100

def blankGrid():
    grid = []
    for col in range(int(size[1]/gridSize)):
        grid.append([])
        for row in range(int(size[0]/gridSize)):
            grid[-1].append([])
    return grid

class Main:
    def __init__(self):
        self.STARTING_POPULATION = 20
        self.STARTING_FOOD = 100
        self.FOOD_REGEN = 0.4
        
        self.statsFont = pygame.font.Font(None, 36)

        self.frameNo = 0

        self.settings = [
            ["Fast Mode", False],
            ["Org Stats", False],
            ["Org Sight", False],
            ["Org Brain", False]
        ]

        self.foodSpawn = 0
                
        self.orgGrid = blankGrid()
        self.foodGrid = blankGrid()

        self.orgList = []
        self.foodList = []

        # Create Random Organisms
        for orgNum in range(self.STARTING_POPULATION):
            randPos = [random.random()*size[0], random.random()*size[1]]
            row = math.floor(randPos[0]/gridSize)
            col = math.floor(randPos[1]/gridSize)
            self.orgList.append(Organism(randPos))
            self.orgGrid[col][row].append(orgNum)

        # Create Random Food
        for foodNum in range(self.STARTING_FOOD):
            randPos = [random.random()*size[0], random.random()*size[1]]
            row = math.floor(randPos[0]/gridSize)
            col = math.floor(randPos[1]/gridSize)
            self.foodList.append(Food(randPos))
            self.foodGrid[col][row].append(foodNum)
            

        self.selectedOrganism = None

        self.pressingOne = False
        self.pressingTwo = False
        
    def mainLoop(self):
        self.frameNo += 1
        
        for event in pygame.event.get():    # User did something
            if event.type == pygame.QUIT:   # If user clicked close
                print("User tried to quit")
                global done
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(self.settings)):
                    settingRect = pygame.Rect([10, 200+40*i, 170, 35])
                    if funcs.pointInRect(mousePos, settingRect):
                        self.settings[i][1] = not self.settings[i][1]
                        break
                row = math.floor(mousePos[0]/gridSize)
                col = math.floor(mousePos[1]/gridSize)
                for orgNum in self.orgGrid[col][row]:
                    if self.orgList[orgNum].distanceFrom(mousePos) < self.orgList[orgNum].size:
                        self.selectedOrganism = self.orgList[orgNum]
                        break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.pressingOne = True
                elif event.key == pygame.K_2:
                    self.pressingTwo = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_1:
                    self.pressingOne = False
                if event.key == pygame.K_2:
                    self.pressingTwo = False

        if len(main.orgList) > 0:
            if self.pressingOne:
                main.orgList[0].dir -= 3*deltaTime
            if self.pressingTwo:
                main.orgList[0].dir += 3*deltaTime
                
                
        # MAIN UPDATE CODE
        self.update()

        self.render()

    def render(self):
        screen.fill(colours.GREY(230))

        # Backgroud grid
        self.drawGrid()

        # Surrounding Border
        pygame.draw.rect(screen, colours.RED, screenRect, 3)

        
        for organism in self.orgList:    # Render each organism
            organism.render()

        for food in self.foodList:
            food.render()   # Render each food piece
            

        if main.settings[3][1] and self.selectedOrganism != None:
            self.drawBrain()

        self.renderSettings()

        fpsText = self.statsFont.render("FPS: " + str(round(clock.get_fps(),2)), 0,  colours.RED)
        screen.blit(fpsText, [10,10])
        frameText = self.statsFont.render("Frame No." + str(self.frameNo), 0,  colours.RED)
        screen.blit(frameText, [10,40])
        secondsText = self.statsFont.render("Ingame Seconds: " + str(int(self.frameNo/FPS)), 0,  colours.RED)
        screen.blit(secondsText, [10,70])
        organismText = self.statsFont.render("Organism Count: " + str(len(self.orgList)), 0,  colours.RED)
        screen.blit(organismText, [10,100])
        foodText = self.statsFont.render("Food Count: " + str(len(self.foodList)), 0,  colours.RED)
        screen.blit(foodText, [10,130])

    def renderSettings(self):
        for i in range(len(self.settings)):
            settingRect = pygame.Rect([10, 200+40*i, 170, 35])
            pygame.draw.rect(screen, colours.GREY(150), settingRect)
            circlePos = funcs.arrRound([settingRect.x + settingRect.h/2, settingRect.centery])
            if self.settings[i][1]:
                pygame.draw.circle(screen, colours.DARK_GREEN, circlePos, int(settingRect.h*0.4))
            else:
                pygame.draw.circle(screen, colours.RED, circlePos, int(settingRect.h*0.4))
                
            settingText = self.statsFont.render(self.settings[i][0], 0,  colours.BLACK)
            textRect = settingText.get_rect()
            textRect.midleft = [settingRect.x + settingRect.h, settingRect.centery]
            screen.blit(settingText, textRect.topleft)

    def update(self):
        ## First update all the grid positions to be used
        self.orgGrid = blankGrid()
        for orgNum in range(len(self.orgList)):
            gridPos = self.orgList[orgNum].gridPos
            self.orgGrid[gridPos[1]][gridPos[0]].append(orgNum)

        ## Update each organism using new grid positions
        for organism in self.orgList:
            organism.update()

        ## After updating, remove dead organisms
        for orgNum in range(len(self.orgList)-1, -1, -1):
            if self.orgList[orgNum].energy <= 0:
                self.orgList.pop(orgNum)

        ## Add a piece of food if any are missing
        if len(self.foodList) < self.STARTING_FOOD and self.foodSpawn <= 0:
            self.foodSpawn = self.FOOD_REGEN
            randPos = [random.random()*size[0], random.random()*size[1]]
            row = math.floor(randPos[0]/gridSize)
            col = math.floor(randPos[1]/gridSize)
            self.foodList.append(Food(randPos))
            self.foodGrid[col][row].append(len(self.foodList)-1)
        self.foodSpawn -= deltaTime
                
    def drawGrid(self):
        for col in range(len(self.orgGrid)):
            pygame.draw.line(screen, colours.GREY(200), [0, gridSize*col], [size[0], gridSize*col], 4)
        for row in range(len(self.orgGrid[0])):
            pygame.draw.line(screen, colours.GREY(200), [gridSize*row, 0], [gridSize*row, size[1]], 4)

    def drawBrain(self):
        drawRect = [20,630,300,250]
        pygame.draw.rect(screen, colours.GREY(200), drawRect)

        bugBrain = self.selectedOrganism.brain
        brainLayout = []

        for layerNum in range(len(bugBrain.layers)):
            layer = bugBrain.layers[layerNum]
            layerLength = len(layer)
            if layerNum != len(bugBrain.layers)-1:
                layerLength -= 1

            neuronX = int(drawRect[0] + (layerNum+0.5)*(drawRect[2]/len(bugBrain.layers)))
            brainLayout.append([])
            
            for neuronNum in range(layerLength):
                neuronY = int(drawRect[1] + (neuronNum+0.5)*(drawRect[3]/layerLength))
                brainLayout[-1].append([neuronX, neuronY])

        for layerNum in range(len(brainLayout)-1):
            for neuronNum in range(len(brainLayout[layerNum])):
                for weight in range(len(bugBrain.layers[layerNum][neuronNum])):   # draw connecting lines
                    lineColour = colours.BLUE
                    if bugBrain.layers[layerNum][neuronNum][weight] < 0:
                        lineColour = colours.RED
                    lineWidth = 1 + int(4 * abs(bugBrain.layers[layerNum][neuronNum][weight]))
                    pygame.draw.line(screen, lineColour, brainLayout[layerNum][neuronNum], brainLayout[layerNum+1][weight], lineWidth)


        for layerNum in range(len(brainLayout)):
            for neuronNum in range(len(brainLayout[layerNum])):
                neuronColour = colours.DARK_GREEN
                neuronSize = 25
                if layerNum > 0:
                    neuronColour = colours.BLUE
                    if bugBrain.layers[layerNum-1][-1][neuronNum] < 0:
                        neuronColour = colours.RED
                    neuronSize = 10 + int(4 * abs(bugBrain.layers[layerNum-1][-1][neuronNum]))
                pygame.draw.circle(screen, neuronColour, brainLayout[layerNum][neuronNum], neuronSize)
                pygame.draw.circle(screen, colours.BLACK, brainLayout[layerNum][neuronNum], neuronSize, 2)


class Organism:
    def __init__(self, pos, parent=None):
        self.pos = pos
        self.gridPos = [math.floor(self.pos[0]/gridSize), math.floor(self.pos[1]/gridSize)]
        self.dir = 0
        
        self.size = 10     # radius of organism
        self.speed = 50

        self.brainUsage = 0.2   # Timer between uses of the brain
        self.brainClock = 0     # A clock to keep track of time since brain last used
        
        self.turnAmount = 0
        self.moveAmount = 0

        if parent == None:
            self.brain = neural_net.Neural_Network([3,2,2])
        else:
            self.brain = parent.brain.childBrain()

        self.neuronCount = 0
        for layerNum in range(1, len(self.brain.layers)-1):
            self.neuronCount += len(self.brain.layers[layerNum])-1

        # Life Stats
        self.energy = 50   # out of 100

        # Sight Variables
        self.VIEW_RANGE = 200 # How many pixels far organism can see
        self.VIEW_ANGLE = 1  # In radians (2*pi = 360 degrees)
        self.VIEW_LINES = 3  # Number of lines seperating segments for organisms sight (one less segment than lines)
        self.viewPointList = [] # End points of each sight lines counterclockwise to clockwise

    def render(self):
        for endPoint in self.viewPointList:
            pygame.draw.line(screen, colours.GREY(200), funcs.arrRound(self.pos), funcs.arrRound(endPoint), int(self.size/3))
        
        lineEnd = funcs.extendLine(self.pos, self.dir, self.size*1.5)
        pygame.draw.line(screen, colours.BLACK, funcs.arrRound(self.pos), funcs.arrRound(lineEnd), int(self.size/3))
        pygame.draw.circle(screen, colours.BLACK, funcs.arrRound(lineEnd), int(self.size/4))
        
        pygame.draw.circle(screen, colours.ORANGE, funcs.arrRound(self.pos), int(self.size))

        if main.settings[1][1]:
            self.renderStats()

    def renderStats(self):
        statRect = pygame.Rect(self.pos[0]+self.size*2, self.pos[1]-self.size*4, self.size, self.size*8)
        
        energyRect = statRect.copy()
        energyBar = energyRect.copy()
        energyBar.height = energyBar.height * (self.energy/100)
        energyBar.bottom = energyRect.bottom
        pygame.draw.rect(screen, colours.RED, energyBar)
        pygame.draw.rect(screen, colours.BLACK, energyRect, 2)

        speedRect = statRect.copy()
        speedRect.x += self.size*1.5
        speedBar = speedRect.copy()
        speedBar.height = speedBar.height * self.moveAmount
        speedBar.bottom = speedRect.bottom
        pygame.draw.rect(screen, colours.DARK_GREEN, speedBar)
        pygame.draw.rect(screen, colours.BLACK, speedRect, 2)

        turnRect = statRect.copy()
        turnRect.x += self.size*3
        turnBar = turnRect.copy()
        turnBar.top = turnBar.centery
        turnBar.height = (turnBar.height/2) * self.turnAmount
        pygame.draw.rect(screen, colours.BLUE, turnBar)
        pygame.draw.rect(screen, colours.BLACK, turnRect, 2)
        pygame.draw.line(screen, colours.BLACK, turnRect.midleft, turnRect.midright, 2)
        

    def update(self):
        if self.brainClock <= 0:
            brainInput = [0] * self.VIEW_LINES
            
            seenFood = self.nearbyFood(self.size + 5 + self.VIEW_RANGE)
            for foodArr in seenFood:
                foodObject = main.foodList[foodArr[0]]
                relativePos = [foodObject.pos[0]+foodArr[1], foodObject.pos[1]+foodArr[2]]
                foodDist = self.distanceFrom(relativePos)
                if foodDist < self.VIEW_RANGE:
                    eyeNum = self.eyeCanSee(relativePos)
                    if eyeNum != None:
                        brainInput[eyeNum] += foodDist / self.VIEW_RANGE
                        

            #print(brainInput)
            brainOutput = self.brain.giveOutput(brainInput)

            self.brainClock = self.brainUsage
            self.turnAmount = brainOutput[0]    # -1 to 1   
            self.moveAmount = (brainOutput[1]+1)/2  # 0 to 1
        else:
            self.brainClock -= deltaTime
            
        self.turnSelf()
        self.moveSelf()

        # Test collision with food
        foodPieces = self.nearbyFood(self.size+5)   # Add food size to the testing radius
        for foodArr in foodPieces:  # Test each food inside the organisms grid square
            foodObject = main.foodList[foodArr[0]]
            relativePos = [foodObject.pos[0]+foodArr[1], foodObject.pos[1]+foodArr[2]]
            if self.distanceFrom(relativePos) < self.size + foodObject.size:   # Organism touching food
                self.energy += foodObject.energy
                if self.energy >= 100:  # Reproduce
                    self.energy = 50
                    main.orgList.append(Organism(self.pos, self))
                    main.orgGrid[self.gridPos[1]][self.gridPos[0]].append(len(main.orgList))
                main.foodList.pop(foodArr[0])
                # Reset food grid each time food is destroyed
                main.foodGrid = blankGrid()
                for foodNum in range(len(main.foodList)):
                    gridPos = main.foodList[foodNum].gridPos
                    main.foodGrid[gridPos[1]][gridPos[0]].append(foodNum)        
                break

        # Energy loss rate depends on: 5 parts speed, 3 parts turning, 2 parts living
        #   Also parts equal to brains hidden layer neuron count
        self.energy -= deltaTime * (0.2 + 0.5*self.moveAmount + 0.3*abs(self.turnAmount) + self.neuronCount*0.1)

        # Rendering view lines
        self.viewPointList = []
        if main.settings[2][1]:
            for lineNum in range(self.VIEW_LINES+1):
                lineAngle = self.dir + lineNum * (self.VIEW_ANGLE/self.VIEW_LINES) - self.VIEW_ANGLE/2
                linePoint = funcs.extendLine(self.pos, lineAngle, self.VIEW_RANGE)
                self.viewPointList.append(linePoint)

    def turnSelf(self):
        self.dir += self.turnAmount * deltaTime
        if self.dir < 0:
            self.dir += 2*math.pi
        if self.dir >= 2*math.pi:
            self.dir -= 2*math.pi

    def moveSelf(self):
        self.pos = funcs.extendLine(self.pos, self.dir, self.speed * self.moveAmount * deltaTime)
        if self.pos[0] < 0:
            self.pos[0] += size[0]
        elif self.pos[0] >= size[0]:
            self.pos[0] -= size[0]
            
        if self.pos[1] < 0:
            self.pos[1] += size[1]
        elif self.pos[1] >= size[1]:
            self.pos[1] -= size[1]
        
        self.gridPos = [math.floor(self.pos[0]/gridSize), math.floor(self.pos[1]/gridSize)]

    def distanceFrom(self, point):
        xDist = abs(point[0] - self.pos[0])
        yDist = abs(point[1] - self.pos[1])
        return math.hypot(xDist, yDist)

    def bearingTo(self, point):
        xDist = point[0] - self.pos[0]
        yDist = point[1] - self.pos[1]
        bearing = math.atan2(yDist,xDist)
        if bearing < 0:
            return bearing + 2*math.pi
        return bearing

    def nearbyFood(self, radius):  # If testing collision with food radius should be food radius + organisms radius
        squareRadius = math.ceil(radius / gridSize) # The radius of squares around organism
        foodPieces = []    # Contains each food number within testing radius of organism, also contains whether object is across map on x and y
        for row in range(-squareRadius, squareRadius+1):
            for col in range(-squareRadius, squareRadius+1):
                gridPos = [row + self.gridPos[0], col + self.gridPos[1]]
                realX = 0
                realY = 0
                if gridPos[0] < 0:
                    gridPos[0] += len(main.foodGrid[0])
                    realX = -size[0]
                elif gridPos[0] >= len(main.foodGrid[0]):
                    gridPos[0] -= len(main.foodGrid[0])
                    realX = size[0]
                if gridPos[1] < 0:
                    gridPos[1] += len(main.foodGrid)
                    realY = -size[1]
                elif gridPos[1] >= len(main.foodGrid):
                    gridPos[1] -= len(main.foodGrid)
                    realY = size[1]
                for foodNum in main.foodGrid[gridPos[1]][gridPos[0]]:
                    foodPieces.append([foodNum, realX, realY])
        return foodPieces

    def eyeCanSee(self, point): # Returns the eye that a point is inside
        foodAngle = self.bearingTo(point)
        dirOffset = foodAngle - self.dir
        if dirOffset > math.pi:
            dirOffset -= 2*math.pi
        elif dirOffset < -math.pi:
            dirOffset += 2*math.pi

        if abs(dirOffset) <= self.VIEW_ANGLE/2:
            dirOffset += self.VIEW_ANGLE/2      # Make angle range from zero to view angle
            eyeSize = self.VIEW_ANGLE / self.VIEW_LINES
            eyeNum = math.floor(dirOffset / eyeSize)
            return eyeNum

        return None
        

class Food:
    def __init__(self, pos):
        self.pos = pos
        self.gridPos = [math.floor(self.pos[0]/gridSize), math.floor(self.pos[1]/gridSize)]

        self.size = 5

        self.energy = 10

        self.colour = colours.BLUE

    def render(self):
        pygame.draw.circle(screen, self.colour, funcs.arrRound(self.pos), int(self.size))
        self.colour = colours.BLUE


screenRect = pygame.Rect(0,0,size[0],size[1])
screenCenter = screenRect.center

font36 = pygame.font.Font(None, 36)
font24 = pygame.font.Font(None, 24)

print("Food Seeking Organisms... \n")

clock = pygame.time.Clock()
FPS = 60
deltaTime = 1 / FPS
done = False
main = Main()
 
# -------- Main Program Loop -----------
while not done:
    mousePos = pygame.mouse.get_pos()

    main.mainLoop()
    
    pygame.display.update()

    if main.settings[0][1]:
        clock.tick()
    else:
        clock.tick(FPS)
    
pygame.quit()
print("User Quit")
























