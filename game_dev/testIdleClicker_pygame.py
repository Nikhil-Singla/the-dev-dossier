## To use Python in CMD, use py instead of python
## Idle clicker game, Turret Auto Tower Defense

import pygame  
pygame.init()

screen = pygame.dislpay.set_mode([1080, 720])
pygame.display.set_caption('Idle Turret Maker')

gameState = True ## Game Running
while gameState:

    for event in pygame.event.get():
        if event.type() == pygame.QUIT: ## Different from quit(). Here, its an event
            gameState = False

pygame.quit() ## Uninitialize all pygame modules
