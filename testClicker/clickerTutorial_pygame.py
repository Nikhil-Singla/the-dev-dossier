## To use Python in CMD, use py instead of python
## Idle clicker game
## Following tutorial by : LeMaster Tech on YouTube

import pygame  
pygame.init()

## Color Palette = (R, G, B) values
aqua = (0,255,255)
navy = (0,0,205)
black = (0,0,0)
skin = (255,228,196)
orange = (255,97,3)
metallic = (198,226,255)
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
## End Palette

screen = pygame.display.set_mode([1080, 720]) ## Resolution
pygame.display.set_caption('Not Adventure Capitalist') ## Title of the game

background = black  ## Variable that can be edited later
frameRate = 60  ## Framerate 

font = pygame.font.Font('freesansbold.ttf', 16) ## Font
timer = pygame.time.Clock() ## Help run our game at 60 FPS

buttonColorsOrder = [white, red, aqua, orange, navy]
verticalPositionOrder = [100, 200, 300, 400, 500]

## Game Variables

moneyOnButtonPress = [1, 2, 3, 4, 5]    # Upgrade of Box One, Two, Three. . .    Tells about the money gained on button press
barFillingSpeed = [5, 4, 3, 2, 1]       # Upgrade of speed_One, Two, Three. . .  Tells about the speed of the bar filling
percentFillForI = [0] * 5               # Upgrade of length_One , Two, Three. . .Tells of the current filling percent
totalMoneyEarned = 0                    # Upgrade of Score                       Tells of the total money earned
drawBarFilling = [False] * 5            # Upgrade of draw_One , Two, Three. . .  Tells if the bar is being drawn

## End Game Variables

## Manager Variables
managerOwned = [False] * 5              # Upgrade of manFiveOne, Two, Three. . . Tells if the manager is owned 
managerCost = [100, 200, 300, 400, 500] # Upgrade of manOneCost, Two, Three. . . Tells what the cost of the manager is
buttonUpgradeCost = list(range(5))      # Upgrade of oneCost , Two ,  Three. . . Tells about the current and start cost of the button upgrade.

oneCost = 1
manOneOwn = False
managerCost[0] = 100

twoCost = 2
manTwoOwn = False
managerCost[1] = 500

threeCost = 3
manThreeOwn = False
managerCost[2] = 1000

fourCost = 4
manFourOwn = False
managerCost[3] = 3000

fiveCost = 5
manFiveOwn = False
managerCost[4] = 5000

## End Manager Variables

def draw_Box(color, y_cord, value, draw, length, speed):
    global totalMoneyEarned
    if draw and length < 200:
        length += speed
    elif length >= 200:
        draw = False
        length = 0
        totalMoneyEarned += value

    pygame.draw.rect(screen, color, [70, y_cord-15, 200, 30], 2)
    pygame.draw.rect(screen, color, [70, y_cord-15, length, 30])
    task = pygame.draw.circle(screen, color, (30, y_cord), 20, 5)
    value_text = font.render(str(round(value,1)), True, white)
    screen.blit(value_text, (16, y_cord-10))
    return task, length, draw

def newButton(color, x_coord, cost, manCost, owned):
    color_button = pygame.draw.rect(screen, color, [x_coord, 600, 50, 30])
    color_cost = font.render(str(round(cost,1)), True, black)
    screen.blit(color_cost, (x_coord+6, 605))
    if not owned:
        managerButton = pygame.draw.rect(screen, color, [x_coord, 670, 50, 30])
        managerText = font.render(str(round(manCost,1)), True, black)
        screen.blit(managerText, (x_coord+6, 675))
    else:
        managerButton = pygame.draw.rect(screen, black, [x_coord, 670, 50, 30])
    return color_button, managerButton

gameState = True ## Game Running
while gameState:
    timer.tick(frameRate) ## Tick at the specified framerate
    if manOneOwn and not drawBarFilling[0]:
        drawBarFilling[0] = True
    if manTwoOwn and not drawBarFilling[1]:
        drawBarFilling[1] = True
    if manThreeOwn and not drawBarFilling[2]:
        drawBarFilling[2] = True
    if manFourOwn and not drawBarFilling[3]:
        drawBarFilling[3] = True
    if manFiveOwn and not drawBarFilling[4]:
        drawBarFilling[4] = True
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: ## Different from quit(). Here, its an event
            gameState = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(5):
                if tasks[i].collidepoint(event.pos):
                    drawBarFilling[i] = True

            if manBuy1.collidepoint(event.pos) and totalMoneyEarned >= managerCost[0] and not manOneOwn:
                manOneOwn = True
                totalMoneyEarned -= managerCost[0]
            if manBuy2.collidepoint(event.pos) and totalMoneyEarned >= managerCost[1] and not manTwoOwn:
                manTwoOwn = True
                totalMoneyEarned -= managerCost[1]
            if manBuy3.collidepoint(event.pos) and totalMoneyEarned >= managerCost[2] and not manThreeOwn:
                manThreeOwn = True
                totalMoneyEarned -= managerCost[2]
            if manBuy4.collidepoint(event.pos) and totalMoneyEarned >= managerCost[3] and not manFourOwn:
                manFourOwn = True
                totalMoneyEarned -= managerCost[3]
            if manBuy5.collidepoint(event.pos) and totalMoneyEarned >= managerCost[4] and not manFiveOwn:
                manFiveOwn = True
                totalMoneyEarned -= managerCost[4]
            if buy1.collidepoint(event.pos) and totalMoneyEarned >= oneCost:
                if oneCost < 500:
                    moneyOnButtonPress[0] += 1
                    totalMoneyEarned -= oneCost
                    oneCost *= 1.2
                else:
                    moneyOnButtonPress[0] += 2
                    totalMoneyEarned -= oneCost
                    oneCost *= 1.1
            if buy2.collidepoint(event.pos) and totalMoneyEarned >= twoCost:
                if twoCost < 1000:
                    moneyOnButtonPress[1] += 1.5
                    totalMoneyEarned -= twoCost
                    twoCost *= 1.35
                else:
                    moneyOnButtonPress[1] += 3
                    totalMoneyEarned -= twoCost
                    twoCost *= 1.25
            if buy3.collidepoint(event.pos) and totalMoneyEarned >= threeCost:
                if threeCost < 1500:
                    moneyOnButtonPress[2] += 5
                    totalMoneyEarned -= threeCost
                    threeCost *= 1.5
                else:
                    moneyOnButtonPress[2] += 10
                    totalMoneyEarned -= threeCost
                    threeCost *= 1.4
            if buy4.collidepoint(event.pos) and totalMoneyEarned >= fourCost:
                if fourCost < 2000:
                    moneyOnButtonPress[3] += 30
                    totalMoneyEarned -= fourCost
                    fourCost *= 1.8
                else:
                    moneyOnButtonPress[3] += 40
                    totalMoneyEarned -= fourCost
                    fourCost *= 1.6
            if buy5.collidepoint(event.pos) and totalMoneyEarned >= fiveCost:
                if fiveCost < 5000:
                    moneyOnButtonPress[4] += 100
                    totalMoneyEarned -= fiveCost
                    fiveCost *= 2
                else:
                    moneyOnButtonPress[4] += 200
                    totalMoneyEarned -= fiveCost
                    fiveCost *= 1.6
            
            
    screen.fill(background) ## Have our initial background on the screen
    
    tasks = []
    for i in range(5):
        tempTask, percentFillForI[i], drawBarFilling[i] = draw_Box(buttonColorsOrder[i], verticalPositionOrder[i], moneyOnButtonPress[i], drawBarFilling[i], percentFillForI[i], barFillingSpeed[i])
        tasks.append(tempTask)

    buy1, manBuy1 = newButton(white, 10, oneCost, managerCost[0], manOneOwn)
    buy2, manBuy2 = newButton(red, 80, twoCost, managerCost[1], manTwoOwn)
    buy3, manBuy3 = newButton(aqua, 150, threeCost, managerCost[2], manThreeOwn)
    buy4, manBuy4 = newButton(orange, 220, fourCost, managerCost[3], manFourOwn)
    buy5, manBuy5 = newButton(navy, 290, fiveCost, managerCost[4], manFiveOwn)

    displayMoney = font.render('Money: $'+str(round(totalMoneyEarned,2)), True, white, black)
    screen.blit(displayMoney, (10,5))

    buyMore = font.render('Buy More: ', True, white)
    screen.blit(buyMore, (10, 580))

    buyMoreMan = font.render('Buy Managers: ', True, white)
    screen.blit(buyMoreMan, (10, 650))

    pygame.display.flip() ## Update the content of the entire display

pygame.quit() ## Uninitialize all pygame modules
