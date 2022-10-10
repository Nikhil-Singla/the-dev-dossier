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
pygame.display.set_caption('Idle Turret Maker') ## Title of the game

background = black ## Variable that can be edited later
frameRate = 60  ## Framerate 
font = pygame.font.Font('freesansbold.ttf', 16) ## Font

timer = pygame.time.Clock() ## Help run our game at 60 FPS

def draw_Box(color, x_coord):
    pygame.draw.rect(screen, color, [x_coord, 500, 100, 100], 2)

def draw_endBox(color, x_coord):
    pygame.draw.rect(screen, color, [x_coord, 500, 100, 100], 2)
    pygame.draw.line(screen, color, (x_coord+50, 525), (x_coord+50, 575), 3)
    pygame.draw.line(screen, color, (x_coord+25, 550), (x_coord+75, 550), 3)

boxCount = 2

gameState = True ## Game Running
while gameState:
    timer.tick(frameRate) ## Tick at the specified framerate
    for event in pygame.event.get():
        if event.type == pygame.QUIT: ## Different from quit(). Here, its an event
            gameState = False
    screen.fill(background) ## Have our initial background on the screen
    
    draw_Box(white, 100)
    draw_Box(white, 250)
    draw_Box(white, 400)
    draw_endBox(white, 400)

    pygame.display.flip() ## Update the content of the entire display
pygame.quit() ## Uninitialize all pygame modules
