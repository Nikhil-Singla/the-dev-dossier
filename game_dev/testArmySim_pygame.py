## To use Python in CMD, use py instead of python
## Auto Battler
## Army Simulator Game
## Credits: Me <3

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

## Global Variables
screen = pygame.display.set_mode([1080, 720]) ## Resolution
pygame.display.set_caption('Army Sim') ## Title of the game

selectionCount = 0
selectedFighter = []
fightResult = []
beginBattle = False

background = black ## Variable that can be edited later
frameRate = 60  ## Framerate 
font = pygame.font.Font('freesansbold.ttf', 12) ## Font

timer = pygame.time.Clock() ## Help run our game at 60 FPS

## Stat list will be used later to display the four types of stats on screen of each of the troops
displayStat1 = []
displayStat2 = []
displayStat3 = []
displayStat4 = []
## Global Variables END


## Army Stats: [Soldier, Archer, Cavalry]

healthMod = [100, 200, 300]
attackMod = [10, 20, 30]
defenseMod = [30, 20, 10]
speedMod = [3, 2, 1]

## (-> = trumps)
## Infantry -> Archer -> Cavalry -> Infantry 

statList = [healthMod, attackMod, defenseMod, speedMod] ## Put the stats into a 2D Array for ease of access

def turnAttack(attack, speed):
    dmgDealt = max(attack*speed, attack+speed)
    return dmgDealt

def turnDefense(defense, speed):
    dmgBlocked = min(speed*defense, speed+defense)
    return dmgBlocked

def healthLeft(health, block, taken):
    health = health - (taken - block) ## Health is just damage minus whatever is blocked
    if(health < 0): ## KO condition
        health = 0
    return health

def fightTurn(health, speed, attack, defense):
    ## Fighting turn where we get attack, defense and return remaining health of troop after
    attack = turnAttack(attack, speed)
    defend = turnDefense(defense, speed)
    health = healthLeft(health, defend, attack)
    return health

def statDisplay(listVar, index, stat, name):
    ## Inserting the stats (value) into a specified list (listVar) along with their (index) and (name)
    listVar.insert(index, font.render(name+str(round(stat)), True, white, black))

def choose_fighterButton():
    ## Drawing Fighter Button
    pygame.draw.rect(screen, aqua, [400, 50, 150, 25])
    buttonText = font.render(('Choose your fighter: '), True, white)
    screen.blit(buttonText, (406, 50))
    ## Drawing Troop Selection Buttons
    warOne = pygame.draw.rect(screen, red, [395, 75, 50, 25])
    warTwo = pygame.draw.rect(screen, red, [450, 75, 50, 25])
    warThree = pygame.draw.rect(screen, red, [505, 75, 50, 25])
    buttonText = font.render(('Warrior'), True, black)
    screen.blit(buttonText, (397, 77))
    buttonText = font.render(('Archer'), True, black)
    screen.blit(buttonText, (452, 77))
    buttonText = font.render(('Cavalry'), True, black)
    screen.blit(buttonText, (507, 77))
    ## Returning the pygame buttons to select troops
    return warOne, warTwo, warThree

def printBattle(fightList):
    j = 2
    while fightList:
        i = fightList.pop()
        statDisplay(displayStat1, i, healthMod[i], 'HP :')
        statDisplay(displayStat2, i, attackMod[i], 'ATK:')
        statDisplay(displayStat3, i, defenseMod[i], 'DEF:')
        statDisplay(displayStat4, i, speedMod[i], 'SPD:')
        screen.blit(displayStat1.pop(), (100+70*j,200))
        screen.blit(displayStat2.pop(), (100+70*j,240))
        screen.blit(displayStat3.pop(), (100+70*j,280))
        screen.blit(displayStat4.pop(), (100+70*j,320))
        j -= 1

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
screen.fill(background) ## Have our initial background on the screen

while gameState:
    timer.tick(frameRate) ## Tick at the specified framerate
    for event in pygame.event.get():
        if event.type == pygame.QUIT: ## Different from quit(). Here, its an event
            gameState = False

    for i in range(0,3):
        statDisplay(displayStat1, i, healthMod[i], 'HP :')
        statDisplay(displayStat2, i, attackMod[i], 'ATK:')
        statDisplay(displayStat3, i, defenseMod[i], 'DEF:')
        statDisplay(displayStat4, i, speedMod[i], 'SPD:')

    for i in range(0,3):
        screen.blit(displayStat1.pop(), (10+70*i,5))
        screen.blit(displayStat2.pop(), (10+70*i,35))
        screen.blit(displayStat3.pop(), (10+70*i,65))
        screen.blit(displayStat4.pop(), (10+70*i,95))

##    if selectionCount!=0:
##        print(selectionCount)
    infantry, archer, cavalry = choose_fighterButton()

    if selectionCount==2:
        beginBattle = True
        selectionCount = 0

    if beginBattle:
        printBattle(selectedFighter)
        beginBattle = False

    if event.type == pygame.MOUSEBUTTONUP:
        pos = pygame.mouse.get_pos() 
        if infantry.collidepoint(pos):
            selectedFighter.append(2)
            selectionCount += 1
        if archer.collidepoint(pos):
            selectedFighter.append(1)
            selectionCount += 1
        if cavalry.collidepoint(pos):
            selectedFighter.append(0)
            selectionCount += 1
    
    pygame.display.flip() ## Update the content of the entire display

pygame.quit() ## Uninitialize all pygame modules
