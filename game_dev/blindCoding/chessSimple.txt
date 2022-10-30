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
start = pygame.time.get_ticks()

## Game Variables
row = [0]*8
board = [row]*8
pieceName = ["Pawn", "Rook", "Knight", "Bishop", "King", "Queen"]
pieceAmount = [8, 2, 2, 2, 1, 1] ## For Future Customization
pieceValue = [1, 5, 3, 3, 999, 8]
sides = [black, white]
pieceColor = [aqua, navy, orange, green, metallic, red]
boardState = []
sqPieces = {}
piecePos = {}
activePieces = []

class ChessPiece():
    def __init__(self, side, name):
        self.name = name.lower
        self.side = side
        self.value = value()

    def value(self):
        for i in range(len(pieceName)):
            if self.name == pieceName[i].lower():
                return pieceValue[i]
        return 0

    def drawPiece(self, xCor, yCor):
        for i in range(len(pieceName)):
            if self.name == pieceName[i].lower():
                pygame.draw.circle(screen,pieceColor[i], (50*xCor+225, 50*yCor+225), 5)
        return name.lower()
        

def drawSquare(i, j):
    retPiece = NULL    
    if ((i+j)%2 == 0):
        color = white
    else:
        color = brown
    retPiece = pygame.draw.rect(screen,color, [50*i+200, 50*j+200, 50, 50])
    return retPiece

def pawnRow():
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
    boardState.clear()
    addMainPieceRow(False, boardState)      ## True or False for the not yet implemented random
    boardState.append(pawnRow())
    addEmpty(4, boardState)
    boardState.append(pawnRow())
    addMainPieceRow(False, boardState)

def run (time):
    global start
    cooldown = time                    ## Set cooldown = Time (miliseconds)
    now = pygame.time.get_ticks()           ## Get current time
    if now - start >= cooldown:   ## If current time passed is greater than cooldown
        start = now                    ## Change current time
        return True     

gameState = True ## Game Running
screen.fill(background) ## Have our initial background on the screen

def start():
    initBoard()
    
    for j in range(len(sides)):
        tempAmount = pieceAmount.copy()
        for i in range(len(tempAmount)):
            while tempAmount[i] > 0:
                tempAmount[i] -= 1
                piece = ChessPiece(sides[j],pieceName[i])
                activePieces.append(piece)

    for i in range(len(boardState)):
        for j in range(len(boardState[i])):
            name = drawPiece(boardState[i][j], j, i)
            if name != NULL:
                numPiece += 1
                piecePos[numPiece] = name


while gameState:
    sqNumber = 0
    numPiece = 0

    timer.tick(frameRate) ## Tick at the specified framerate
    for event in pygame.event.get():
        if event.type == pygame.QUIT: ## Different from quit(). Here, its an event
            gameState = False

    if run(1000):
        screen.fill(black)
        
        for i in range(len(board)):
            for j in range(len(board[i])):
                    piece = drawSquare(i, j)        ## Drawing Each Square
                    if piece != NULL:
                        sqNumber += 1
                        sqPieces[sqNumber] = piece
        

    pygame.display.flip() ## Update the content of the entire display

for key, value in piecePos.items():
    print(key, value)

pygame.quit() ## Uninitialize all pygame modules

