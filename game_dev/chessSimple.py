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
brown = (225, 193, 110)
## End Palette

length = 800 
breadth = 800

## Global Variables

screen = pygame.display.set_mode([length, breadth]) ## Resolution
pygame.display.set_caption('Chessboard') ## Title of the game
background = black  ## Variable that can be edited later
frameRate = 60  ## Framerate 
font = pygame.font.Font('freesansbold.ttf', 16) ## Font
timer = pygame.time.Clock() ## Help run our game at 60 FPS
timer_interval = 1000 # 0.5 seconds
timer_event = pygame.USEREVENT + 1

row = [0]*8
board = [row]*8



def drawSquare(i, j):
    if ((i+j)%2 == 0):
        color = white
    else:
        color = brown
    pygame.draw.rect(screen,color, [50*i+200, 50*j+200, 50, 50])

pieceName = ["Pawn", "Rook", "Knight", "Bishop", "King", "Queen"]
pieceColor = [aqua, navy, orange, green, metallic, red]
def drawPiece(name, i, j):
    for i in range(len(pieceName)):
        if name.lower() == pieceName[i].lower():
            pygame.draw.circle(screen,pieceColor[i], (50*i+175, 50*j+225), 5)
        

gameState = True ## Game Running
screen.fill(background) ## Have our initial background on the screen
while gameState:
    timer.tick(frameRate) ## Tick at the specified framerate
    for event in pygame.event.get():
        if event.type == pygame.QUIT: ## Different from quit(). Here, its an event
            gameState = False

    for i in range(len(board)):
        for j in range(len(board[i])):
                drawSquare(i, j)

    drawPiece("rook", 0, 0)


    pygame.display.flip() ## Update the content of the entire display

pygame.quit() ## Uninitialize all pygame modules

