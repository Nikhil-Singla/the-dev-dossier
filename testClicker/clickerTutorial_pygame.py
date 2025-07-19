## Idle Clicker Game (Based on LeMaster Tech's YouTube Tutorial)
## Run in CMD using: py yourfilename.py

import pygame  
pygame.init()

# Constants
FIRST_ITEM = 0
SECOND_ITEM = 1

# Color Palette (RGB)
aqua = (0, 255, 255)
navy = (0, 0, 205)
black = (0, 0, 0)
skin = (255, 228, 196)
orange = (255, 97, 3)
metallic = (198, 226, 255)
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)

# Display Setup
screen = pygame.display.set_mode([1080, 720])    # Resolution
pygame.display.set_caption('Not Adventure Capitalist')  # Window Title
background = black
frameRate = 60

# Fonts and Timing
font = pygame.font.Font('freesansbold.ttf', 16)
timer = pygame.time.Clock()

# Button Configuration
buttonColorsOrder = [white, red, aqua, orange, navy]
verticalPositionOrder = [100, 200, 300, 400, 500]
horizontalPositionOrder = [10, 80, 150, 220, 290]

# Upgrade Scaling Factors: (pre-lategame, post-lategame)
buttonUpgradeScalingFactor = [(1.2, 1.1), (1.35, 1.25), (1.5, 1.4), (1.8, 1.6), (2, 1.6)]

# Money Increase per Upgrade: (pre-lategame, post-lategame)
moneyIncreasePerUpgrade = [(1, 2), (1.5, 3), (5, 10), (30, 40), (100, 200)]

# Lategame Thresholds per Button
lateGameThreshold = [500, 1000, 1500, 2000, 5000]

# Game State Variables
moneyOnButtonPress = [1, 2, 3, 4, 5]
barFillingSpeed = [5, 4, 3, 2, 1]
percentFillForI = [0] * 5
drawBarFilling = [False] * 5
totalMoneyEarned = 0

# Manager State
managerOwned = [False] * 5
managerCost = [100, 500, 1000, 3000, 5000]
buttonUpgradeCost = list(range(1, 6))

# Drawing Function for the Main Clicker Box
def draw_Box(color, y_cord, value, draw, length, speed):
    global totalMoneyEarned

    # Update fill bar
    if draw and length < 200:
        length += speed
    elif length >= 200:
        draw = False
        length = 0
        totalMoneyEarned += value

    # Draw box outline and fill
    pygame.draw.rect(screen, color, [70, y_cord - 15, 200, 30], 2)
    pygame.draw.rect(screen, color, [70, y_cord - 15, length, 30])
    
    # Draw clickable circle
    task = pygame.draw.circle(screen, color, (30, y_cord), 20, 5)
    
    # Show money value on the button
    value_text = font.render(str(round(value, 1)), True, white)
    screen.blit(value_text, (16, y_cord - 10))

    return task, length, draw

# Drawing Function for Upgrade and Manager Buttons
def newButton(color, x_coord, cost, manCost, owned):
    # Upgrade button
    color_button = pygame.draw.rect(screen, color, [x_coord, 600, 50, 30])
    color_cost = font.render(str(round(cost, 1)), True, black)
    screen.blit(color_cost, (x_coord + 6, 605))

    # Manager button (disabled if already owned)
    if not owned:
        managerButton = pygame.draw.rect(screen, color, [x_coord, 670, 50, 30])
        managerText = font.render(str(round(manCost, 1)), True, black)
        screen.blit(managerText, (x_coord + 6, 675))
    else:
        managerButton = pygame.draw.rect(screen, black, [x_coord, 670, 50, 30])

    return color_button, managerButton

# ---------------------- Game Loop ----------------------
gameState = True
while gameState:
    timer.tick(frameRate)

    # Managers auto-click their assigned button
    for i in range(5):
        if managerOwned[i] and not drawBarFilling[i]:
            drawBarFilling[i] = True

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameState = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Handle manual clicks on buttons
            for i in range(5):
                if tasks[i].collidepoint(event.pos):
                    drawBarFilling[i] = True

            # Handle manager purchases
            for i in range(5):
                if (managerBuyButtons[i].collidepoint(event.pos)
                    and totalMoneyEarned >= managerCost[i]
                    and not managerOwned[i]):
                    managerOwned[i] = True
                    totalMoneyEarned -= managerCost[i]

            # Handle upgrade purchases
            for i in range(5):
                if (buyButtons[i].collidepoint(event.pos)
                    and totalMoneyEarned >= buttonUpgradeCost[i]):

                    totalMoneyEarned -= buttonUpgradeCost[i]

                    if buttonUpgradeCost[i] < lateGameThreshold[i]:
                        moneyOnButtonPress[i] += moneyIncreasePerUpgrade[i][FIRST_ITEM]
                        buttonUpgradeCost[i] *= buttonUpgradeScalingFactor[i][FIRST_ITEM]
                    else:
                        moneyOnButtonPress[i] += moneyIncreasePerUpgrade[i][SECOND_ITEM]
                        buttonUpgradeCost[i] *= buttonUpgradeScalingFactor[i][SECOND_ITEM]

    # Drawing Phase
    screen.fill(background)

    # Draw clicker bars
    tasks = []
    for i in range(5):
        task, percentFillForI[i], drawBarFilling[i] = draw_Box(
            buttonColorsOrder[i], verticalPositionOrder[i],
            moneyOnButtonPress[i], drawBarFilling[i],
            percentFillForI[i], barFillingSpeed[i]
        )
        tasks.append(task)

    # Draw upgrade and manager buttons
    buyButtons = []
    managerBuyButtons = []
    for i in range(5):
        buyBtn, manBtn = newButton(
            buttonColorsOrder[i], horizontalPositionOrder[i],
            buttonUpgradeCost[i], managerCost[i], managerOwned[i]
        )
        buyButtons.append(buyBtn)
        managerBuyButtons.append(manBtn)

    # Display HUD
    displayMoney = font.render(f'Money: ${round(totalMoneyEarned, 2)}', True, white, black)
    screen.blit(displayMoney, (10, 5))

    screen.blit(font.render('Buy More: ', True, white), (10, 580))
    screen.blit(font.render('Buy Managers: ', True, white), (10, 650))

    pygame.display.flip()  # Refresh screen

# Exit Game
pygame.quit()
