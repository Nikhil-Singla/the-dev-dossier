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

background = black ## Variable that can be edited later
frameRate = 60  ## Framerate 
font = pygame.font.Font('freesansbold.ttf', 16) ## Font

timer = pygame.time.Clock() ## Help run our game at 60 FPS

## Game Variables
boxOne = 1
boxTwo = 2
boxThree = 3
boxFour = 4
boxFive = 5
score = 0
draw_One = False
draw_Two = False
draw_Three = False
draw_Four = False
draw_Five = False

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
    pygame.draw.circle(screen, color, (30, y_cord), 20, 5)
    value_text = font.render(str(value), True, white)
    screen.blit(value_text, (16, y_cord-10))
    return task, length, draw

gameState = True ## Game Running
while gameState:
    timer.tick(frameRate) ## Tick at the specified framerate
    for event in pygame.event.get():
        if event.type == pygame.QUIT: ## Different from quit(). Here, its an event
            gameState = False
    screen.fill(background) ## Have our initial background on the screen
    
    draw_Box(white, 100, boxOne)
    draw_Box(red, 200, boxTwo)
    draw_Box(aqua, 300, boxThree)
    draw_Box(metallic, 400, boxFour)
    draw_Box(navy, 500, boxFive)
    pygame.display.flip() ## Update the content of the entire display

pygame.quit() ## Uninitialize all pygame modules
