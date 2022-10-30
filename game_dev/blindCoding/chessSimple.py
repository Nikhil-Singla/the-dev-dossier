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

class funcTimer():
    def __init__(self):
        self.start = pygame.time.get_ticks()    ## Clock starting

    def run(self, time):
        self.cooldown = time                    ## Set cooldown = Time (miliseconds)
        now = pygame.time.get_ticks()           ## Get current time
        if now - self.start >= self.cooldown:   ## If current time passed is greater than cooldown
            self.start = now                    ## Change current time
            return True                         ## Toggle Value of cooldown return 

## Global Variables
length_of_screen = 800 
breadth_of_screen = 800
display_screen = pygame.display.set_mode([length_of_screen, breadth_of_screen]) ## Resolution
pygame.display.set_caption('Chessboard') ## Title of the game
background_color = black  ## Variable that can be edited later
frameRate = 60  ## Framerate 
default_global_font = pygame.font.Font('freesansbold.ttf', 16) ## Font
framerate_timer = pygame.time.Clock() ## Help run our game at 60 FPS
event_timer_interval = 1000 # 0.5 seconds
clock_start = pygame.time.get_ticks()
## End Global Variables

## Game Variables

count = 0
empty_rows = [0]*8
board_configuration = []
board_values = [[i+j for i in range(8)] for j in range(8)]

list_pieceName = ["P", "R", "Kn", "B", "K", "Q"]
list_pieceValue = [1, 5, 3, 3, 999, 8]
the_two_sides = [black, white]

num_piece_per_side = [8, 2, 2, 2, 1, 1] ## For Future Customization
## End Game Variables

class ChessPiece():
    def __init__(self, side, name):
        self.name = name
        self.side = side
        self.value = self.piece_value()

    def piece_value(self):
        for i in range(len(list_pieceName)):
            if self.name == list_pieceName[i].lower():
                return list_pieceValue[i]
        return 0

## USEFUL FUNCTIONS
def printList1(input_list):
    for i in range(len(input_list)):
        print(input_list[i], sep = ', ')

def printList2(input_list):
    for i in range(len(input_list)):
        for j in range(len(input_list[i])):
            print(input_list[i][j], sep = ',')
## END OF USEFUL FUNCTIONS

def start_configuration(boolean_random):
    if boolean_random:
        return
    else:
        big_row_line = ["R", "Kn", "B", "Q", "K", "B", "Kn", "R"]
        small_row_line = ["P"]*8
        board_configuration.append(big_row_line)
        board_configuration.append(small_row_line)
        for i in range(4):
            board_configuration.append(empty_rows)
        board_configuration.append(small_row_line)
        board_configuration.append(big_row_line)

start_configuration(False)

gameState = True ## Game Running
display_screen.fill(background_color) ## Have our initial background on the screen
while gameState:
    framerate_timer.tick(frameRate) ## Tick at the specified framerate
    for event in pygame.event.get():
        if event.type == pygame.QUIT: ## Different from quit(). Here, its an event
            gameState = False

    pygame.display.flip() ## Update the content of the entire display

printList2(board_configuration)
printList2(board_values)

pygame.quit() ## Uninitialize all pygame modules