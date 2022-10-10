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

screen = pygame.dislpay.set_mode([1080, 720])
pygame.display.set_caption('Idle Turret Maker')

background = black
frameRate = 60
font = pygame.font.Font('comic.ttf', '16')

gameState = True ## Game Running
while gameState:

    for event in pygame.event.get():
        if event.type() == pygame.QUIT: ## Different from quit(). Here, its an event
            gameState = False

pygame.quit() ## Uninitialize all pygame modules
