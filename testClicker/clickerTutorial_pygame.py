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
horizontalPositionOrder = [10, 80, 150, 220, 290]

## Game Variables

moneyOnButtonPress = [1, 2, 3, 4, 5]    # Upgrade of Box One, Two, Three. . .    Tells about the money gained on button press
barFillingSpeed = [5, 4, 3, 2, 1]       # Upgrade of speed_One, Two, Three. . .  Tells about the speed of the bar filling
percentFillForI = [0] * 5               # Upgrade of length_One , Two, Three. . .Tells of the current filling percent
totalMoneyEarned = 0                    # Upgrade of Score                       Tells of the total money earned
drawBarFilling = [False] * 5            # Upgrade of draw_One , Two, Three. . .  Tells if the bar is being drawn

## End Game Variables

## Manager Variables
managerOwned = [False] * 5                  # Upgrade of manOneOwn , Two, Three. . . Tells if the manager is owned 
managerCost = [100, 500, 1000, 3000, 5000]  # Upgrade of manOneCost, Two, Three. . . Tells what the cost of the manager is
buttonUpgradeCost = list(range(1, 6))       # Upgrade of oneCost , Two ,  Three. . . Tells about the current and start cost of the button upgrade.

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
    for i in range(5):
        if managerOwned[i] and not drawBarFilling[0]:
            drawBarFilling[0] = True
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT: ## Different from quit(). Here, its an event
            gameState = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(5):
                if tasks[i].collidepoint(event.pos):
                    drawBarFilling[i] = True
                
                if managerBuyButtons[i].collidepoint(event.pos) and totalMoneyEarned >= managerCost[i] and not managerOwned[i]:
                    managerOwned[i] = True
                    totalMoneyEarned -= managerCost[i]
            
            
            if buy1.collidepoint(event.pos) and totalMoneyEarned >= buttonUpgradeCost[0]:
                if buttonUpgradeCost[0] < 500:
                    moneyOnButtonPress[0] += 1
                    totalMoneyEarned -= buttonUpgradeCost[0]
                    buttonUpgradeCost[0] *= 1.2
                else:
                    moneyOnButtonPress[0] += 2
                    totalMoneyEarned -= buttonUpgradeCost[0]
                    buttonUpgradeCost[0] *= 1.1
                    
            if buy2.collidepoint(event.pos) and totalMoneyEarned >= buttonUpgradeCost[1]:
                if buttonUpgradeCost[1] < 1000:
                    moneyOnButtonPress[1] += 1.5
                    totalMoneyEarned -= buttonUpgradeCost[1]
                    buttonUpgradeCost[1] *= 1.35
                else:
                    moneyOnButtonPress[1] += 3
                    totalMoneyEarned -= buttonUpgradeCost[1]
                    buttonUpgradeCost[1] *= 1.25
            if buy3.collidepoint(event.pos) and totalMoneyEarned >= buttonUpgradeCost[2]:
                if buttonUpgradeCost[2] < 1500:
                    moneyOnButtonPress[2] += 5
                    totalMoneyEarned -= buttonUpgradeCost[2]
                    buttonUpgradeCost[2] *= 1.5
                else:
                    moneyOnButtonPress[2] += 10
                    totalMoneyEarned -= buttonUpgradeCost[2]
                    buttonUpgradeCost[2] *= 1.4
            if buy4.collidepoint(event.pos) and totalMoneyEarned >= buttonUpgradeCost[3]:
                if buttonUpgradeCost[3] < 2000:
                    moneyOnButtonPress[3] += 30
                    totalMoneyEarned -= buttonUpgradeCost[3]
                    buttonUpgradeCost[3] *= 1.8
                else:
                    moneyOnButtonPress[3] += 40
                    totalMoneyEarned -= buttonUpgradeCost[3]
                    buttonUpgradeCost[3] *= 1.6
            if buy5.collidepoint(event.pos) and totalMoneyEarned >= buttonUpgradeCost[4]:
                if buttonUpgradeCost[4] < 5000:
                    moneyOnButtonPress[4] += 100
                    totalMoneyEarned -= buttonUpgradeCost[4]
                    buttonUpgradeCost[4] *= 2
                else:
                    moneyOnButtonPress[4] += 200
                    totalMoneyEarned -= buttonUpgradeCost[4]
                    buttonUpgradeCost[4] *= 1.6
            
            
    screen.fill(background) ## Have our initial background on the screen
    
    tasks = []
    for i in range(5):
        tempTask, percentFillForI[i], drawBarFilling[i] = draw_Box(buttonColorsOrder[i], verticalPositionOrder[i], moneyOnButtonPress[i], drawBarFilling[i], percentFillForI[i], barFillingSpeed[i])
        tasks.append(tempTask)

    buyButtons, managerBuyButtons = [], []
    for i in range(5):
        tempBuyButton, tempManagerBuyButton = newButton(buttonColorsOrder[i], horizontalPositionOrder[i], buttonUpgradeCost[0], managerCost[0], managerOwned[0])
        buyButtons.append(tempBuyButton)
        managerBuyButtons.append(tempManagerBuyButton)


    buy1, manBuy1 = newButton(white, 10, buttonUpgradeCost[0], managerCost[0], managerOwned[0])
    buy2, manBuy2 = newButton(red, 80, buttonUpgradeCost[1], managerCost[1], managerOwned[1])
    buy3, manBuy3 = newButton(aqua, 150, buttonUpgradeCost[2], managerCost[2], managerOwned[2])
    buy4, manBuy4 = newButton(orange, 220, buttonUpgradeCost[3], managerCost[3], managerOwned[3])
    buy5, manBuy5 = newButton(navy, 290, buttonUpgradeCost[4], managerCost[4], managerOwned[4])

    displayMoney = font.render('Money: $'+str(round(totalMoneyEarned,2)), True, white, black)
    screen.blit(displayMoney, (10,5))

    buyMore = font.render('Buy More: ', True, white)
    screen.blit(buyMore, (10, 580))

    buyMoreMan = font.render('Buy Managers: ', True, white)
    screen.blit(buyMoreMan, (10, 650))

    pygame.display.flip() ## Update the content of the entire display

pygame.quit() ## Uninitialize all pygame modules
