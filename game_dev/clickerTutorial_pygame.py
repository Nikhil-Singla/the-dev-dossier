## To use Python in CMD, use py instead of python
## Idle clicker game, Turret Auto Tower Defense

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

## Game Variables

boxOne = 1
boxTwo = 2
boxThree = 3
boxFour = 4
boxFive = 5
score = 90
draw_One = False
draw_Two = False
draw_Three = False
draw_Four = False
draw_Five = False
length_One = 0
length_Two = 0
length_Three = 0
length_Four = 0
length_Five = 0
speed_One = 5
speed_Two = 4
speed_Three = 3
speed_Four = 2
speed_Five = 1

## End Game Variables

## Manager Variables

oneCost = 1
manOneOwn = False
manOneCost = 100
twoCost = 2
manTwoOwn = False
manTwoCost = 500
threeCost = 3
manThreeOwn = False
manThreeCost = 1000
fourCost = 4
manFourOwn = False
manFourCost = 3000
fiveCost = 5
manFiveOwn = False
manFiveCost = 5000

## End Manager Variables

def draw_Box(color, y_cord, value, draw, length, speed):
    global score
    if draw and length < 200:
        length += speed
    elif length >= 200:
        draw = False
        length = 0
        score += value
    pygame.draw.rect(screen, color, [70, y_cord-15, 200, 30], 2)
    pygame.draw.rect(screen, color, [70, y_cord-15, length, 30])
    task = pygame.draw.circle(screen, color, (30, y_cord), 20, 5)
    value_text = font.render(str(value), True, white)
    screen.blit(value_text, (16, y_cord-10))
    return task, length, draw

def newButton(color, x_coord, cost, manCost, owned):
    color_button = pygame.draw.rect(screen, color, [x_coord, 600, 50, 30])
    color_cost = font.render(str(round(cost, 2)), True, black)
    screen.blit(color_cost, (x_coord+6, 350))
    if not owned:
        managerButton = pygame.draw.rect(screen, color, [x_coord, 670, 50, 30])
        managerText = font.render(str(round(manCost, 2)), True, black)
        screen.blit(managerText, (x_coord+6, 675))
    else:
        managerButton = pygame.draw.rect(screen, black, [x_coord, 670, 50, 30])
    return color_button, managerButton

gameState = True ## Game Running
while gameState:
    timer.tick(frameRate) ## Tick at the specified framerate
    if manOneOwn and not draw_One:
        draw_One = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT: ## Different from quit(). Here, its an event
            gameState = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if task1.collidepoint(event.pos):
                draw_One = True
            if task2.collidepoint(event.pos):
                draw_Two = True
            if task3.collidepoint(event.pos):
                draw_Three = True
            if task4.collidepoint(event.pos):
                draw_Four = True
            if task5.collidepoint(event.pos):
                draw_Five = True
            if manBuy1.collidepoint(event.pos) and score >= manOneCost and not manOneOwn:
                manOneOwn = True
                score -= manOneCost

    screen.fill(background) ## Have our initial background on the screen
    
    task1, length_One, draw_One = draw_Box(white, 100, boxOne, draw_One, length_One, speed_One)
    task2, length_Two, draw_Two = draw_Box(red, 200, boxTwo, draw_Two, length_Two, speed_Two)
    task3, length_Three, draw_Three = draw_Box(aqua, 300, boxThree, draw_Three, length_Three, speed_Three)
    task4, length_Four, draw_Four = draw_Box(orange, 400, boxFour, draw_Four, length_Four, speed_Four)
    task5, length_Five, draw_Five = draw_Box(navy, 500, boxFive, draw_Five, length_Five, speed_Five)
    buy1, manBuy1 = newButton(white, 10, oneCost, manOneCost, manOneOwn)
    buy2, manBuy2 = newButton(red, 80, twoCost, manTwoCost, manTwoOwn)
    buy3, manBuy3 = newButton(aqua, 150, threeCost, manThreeCost, manThreeOwn)
    buy4, manBuy4 = newButton(orange, 220, fourCost, manFourCost, manFourOwn)
    buy5, manBuy5 = newButton(navy, 290, fiveCost, manFiveCost, manFiveOwn)

    display_score = font.render('Money: $'+str(round(score,2)), True, white, black)
    screen.blit(display_score, (10,5))
    buyMore = font.render('Buy More: ', True, white)
    screen.blit(buyMore, (10, 580))
    buyMoreMan = font.render('Buy Managers: ', True, white)
    screen.blit(buyMoreMan, (10, 650))
    pygame.display.flip() ## Update the content of the entire display

pygame.quit() ## Uninitialize all pygame modules
