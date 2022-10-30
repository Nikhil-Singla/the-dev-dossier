## To use Python in CMD, use py instead of python
## Auto Battler
## Army Simulator Game
## Credits: Me <3

from asyncio.windows_events import NULL
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

## Game Variables
row = [0]*8
board = [row]*8
pieceName = ["Pawn", "Rook", "Knight", "Bishop", "King", "Queen"]
pieceAmount = [8, 2, 2, 2, 1, 1] ## For Future Customization
pieceColor = [aqua, navy, orange, green, metallic, red]
boardState = []
sqPieces = {}
piecePos = {}

def drawSquare(i, j):
    retPiece = NULL    
    if ((i+j)%2 == 0):
        color = white
    else:
        color = brown
    retPiece = pygame.draw.rect(screen,color, [50*i+200, 50*j+200, 50, 50])
    return retPiece

def drawPiece(name, xCor, yCor):
    for i in range(len(pieceName)):
        if name.lower() == pieceName[i].lower():
            pygame.draw.circle(screen,pieceColor[i], (50*xCor+225, 50*yCor+225), 5)
    return name.lower()
        
def pawnRow(team):
    rowState = []
    for i in range(8):
        rowState.append(pieceName[0])
    return rowState

def addEmpty(number, boardList):
    emptyRow = [""]*8
    for i in range(number):
        boardList.append(emptyRow)

def addMainPieceRow(random, boardList):
    rowState = []
    if random == True:
        return
    else:
        for i in range(1, 6):
            rowState.append(pieceName[i])
        for i in range(3, 0, -1):
            rowState.append(pieceName[i])
    boardList.append(rowState)

def initBoard():
    addMainPieceRow(False, boardState)
    boardState.append(pawnRow(1))
    addEmpty(4, boardState)
    boardState.append(pawnRow(2))
    addMainPieceRow(False, boardState)

initBoard()

gameState = True ## Game Running
screen.fill(background) ## Have our initial background on the screen

while gameState:
    sqNumber = 0
    numPiece = 0
    timer.tick(frameRate) ## Tick at the specified framerate
    for event in pygame.event.get():
        if event.type == pygame.QUIT: ## Different from quit(). Here, its an event
            gameState = False

    for i in range(len(board)):
        for j in range(len(board[i])):
                piece = drawSquare(i, j)        ## Drawing Each Square
                if piece != NULL:
                    sqNumber += 1
                    sqPieces[sqNumber] = piece
    
    for i in range(len(boardState)):
        for j in range(len(boardState[i])):
            name = drawPiece(boardState[i][j], j, i)
            if name != NULL:
                numPiece += 1
                piecePos[numPiece] = name

    pygame.display.flip() ## Update the content of the entire display

for key, value in piecePos.items():
    print(key, value)

pygame.quit() ## Uninitialize all pygame modules

