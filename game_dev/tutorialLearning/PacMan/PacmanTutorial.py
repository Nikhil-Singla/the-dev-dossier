import pygame
from board import boards
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
blue = (0,0,255)
## End Palette

level = boards #[active_board] for multiple levels
width = 900
height = 950
PI = 3.141592653589793


screen = pygame.display.set_mode([width, height])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)

def draw_board(lvl):
    tile_height = ((height - 50) // 32)   ## 50 Pixels for space to write. And Floor division to round down the tile to the nearest height. 32 Tiles vertically
    tile_width = ((width) // 30)      
    for i in range(len(lvl)):           ## i iterates across the rows of cells / y axis
        for j in range(len(lvl[i])):    ## j iterates across the individual cells in the rows / columns / x axis
            if lvl[i][j] == 1:
                pygame.draw.circle( screen, white, ( (j*tile_width + (0.5*tile_width)), (i*tile_height + (0.5*tile_height)) ), 4 )
            if lvl[i][j] == 2:
                pygame.draw.circle( screen, white, ( (j*tile_width + (0.5*tile_width)), (i*tile_height + (0.5*tile_height)) ), 8 )
            if lvl[i][j] == 3:
                pygame.draw.line( screen, blue, ( (j*tile_width + (0.5*tile_width)), (i*tile_height) ), 
                                                ( (j*tile_width + (0.5*tile_width)), (i*tile_height + tile_height) ), 3)
            if lvl[i][j] == 4:
                pygame.draw.line( screen, red, ( (j*tile_width), (i*tile_height + (0.5*tile_height)) ), 
                                                ( (j*tile_width + tile_width), (i*tile_height + (0.5*tile_height)) ), 3)


gameState = True
while gameState:
    timer.tick(fps)
    screen.fill(black)
    draw_board(level)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameState = False
    
    pygame.display.flip()

pygame.quit()
