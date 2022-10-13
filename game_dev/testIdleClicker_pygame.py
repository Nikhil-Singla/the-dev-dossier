## To use Python in CMD, use py instead of python
## Idle clicker game, Turret Auto Tower Defense

## Army Simulator Game

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

## Army Stats: [Soldier, Archer, Cavalry]

healthMod = [100, 100, 100]
attackMod = [10, 50, 25]
defenseMod = [10, 5, 5]
speedMod = [1, 0, 2]

## (-> = trumps)
## Infantry -> Archer -> Cavalry -> Infantry 

statList = [healthMod, attackMod, defenseMod, speedMod]

def turnAttack(attack, speed):
    dmgDealt = max(attack*speed, attack+speed)
    return dmgDealt

def turnDefens(defense, speed):
    dmgBlocked = min(speed*defense, speed+defense)
    return dmgBlocked

def fightTurn(health, speed, attack, defense):

""""
healthOne = 100
attackOne = 10
defenseOne = 10
speedMod = 1
healthTwo = 100
attackTwo = 40
defenseOne = 5
speedMod = 0
healthThree = 150
attackThree = 20
defenseThree = 5
speedMod = 2
"""

gameState = True ## Game Running
while gameState:
    timer.tick(frameRate) ## Tick at the specified framerate
    for event in pygame.event.get():
        if event.type == pygame.QUIT: ## Different from quit(). Here, its an event
            gameState = False
    screen.fill(background) ## Have our initial background on the screen
    
    pygame.display.flip() ## Update the content of the entire display
pygame.quit() ## Uninitialize all pygame modules
