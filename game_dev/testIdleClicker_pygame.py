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

screen = pygame.display.set_mode([1080, 720])
pygame.display.set_caption('Idle Turret Maker')

background = black
frameRate = 60 
font = pygame.font.Font('freesansbold.ttf', 16)

timer = pygame.time.Clock() ## Help run our game at 60 FPS

gameState = True ## Game Running
while gameState:
    timer.tick(frameRate) ## Tick at the specified framerate
    for event in pygame.event.get():
        if event.type == pygame.QUIT: ## Different from quit(). Here, its an event
            gameState = False
    screen.fill(background) ## Have our initial background on the screen

    pygame.display.flip() ## Flip everything on the screen
pygame.quit() ## Uninitialize all pygame modules
