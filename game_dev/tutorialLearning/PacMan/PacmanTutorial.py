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

wall_color = [blue, red]
pellet_color = [white]

screen = pygame.display.set_mode([width, height])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)
player_images = []

for i in range(1, 5):
    img_loader = pygame.image.load(f'assets/player_images/{i}.png')         ## Load images from assets/player_images/[number from 1, 2, 3, 4].png
    scaled_img = pygame.transform.scale(img_loader), (45, 45)               ## Scale the images to the screen by increasing or decreasing
    player_images.append(scaled_img)                                        ## Append the scaled images in order to the list of images we will use

def draw_board(lvl, wall_i = 0, pellet_i = 0):  ## Lvl is the lvl number in map, wall_i is the index for wall colors, and same for pellet for pellet colors
    tile_height = ((height - 50) // 32)         ## 50 Pixels for space to write. And Floor division to round down the tile to the nearest height. 32 Tiles vertically
    tile_width = ((width) // 30)      
    for i in range(len(lvl)):                   ## i iterates across the rows of cells / y axis
        for j in range(len(lvl[i])):            ## j iterates across the individual cells in the rows / columns / x axis
            if lvl[i][j] == 1:                  ## Drawing Smaller Pellet
                pygame.draw.circle( screen, pellet_color[pellet_i], ( (j*tile_width + (0.5*tile_width)), (i*tile_height + (0.5*tile_height)) ), 4 )     
            if lvl[i][j] == 2:                  ## Drawing Larget Pellet
                pygame.draw.circle( screen, pellet_color[pellet_i], ( (j*tile_width + (0.5*tile_width)), (i*tile_height + (0.5*tile_height)) ), 8 )     
            if lvl[i][j] == 3:                  ## Drawing Vertical Line
                pygame.draw.line( screen, wall_color[wall_i], ( (j*tile_width + (0.5*tile_width)), (i*tile_height) ),                                   
                                                ( (j*tile_width + (0.5*tile_width)), (i*tile_height + tile_height) ), 3)        
            if lvl[i][j] == 4:                  ## Drawing Horizontal Lines
                pygame.draw.line( screen, wall_color[wall_i], ( (j*tile_width), (i*tile_height + (0.5*tile_height)) ),                                  
                                                ( (j*tile_width + tile_width), (i*tile_height + (0.5*tile_height)) ), 3)
            if lvl[i][j] == 5:                  ## Drawing Top Right arc
                pygame.draw.arc( screen, wall_color[wall_i], [(j*tile_width) - (tile_width*0.4) - 2, (i*tile_height + (0.5*tile_height)), tile_width, tile_height], 0, PI/2, 3 )
            if lvl[i][j] == 6:                  ## Drawing Top Left arc
                pygame.draw.arc( screen, wall_color[wall_i], [(j*tile_width) + (tile_width*0.4) + 2, (i*tile_height + (0.5*tile_height) - 1), tile_width, tile_height], PI/2, PI, 3 )
            if lvl[i][j] == 7:                  ## Drawing Bottom Left  arc
                pygame.draw.arc( screen, wall_color[wall_i], [(j*tile_width) + (tile_width*0.5) - 1, (i*tile_height - (0.4*tile_height) - 1), tile_width, tile_height], PI, 3*PI/2, 3 )
            if lvl[i][j] == 8:                  ## Drawing Bottom Right arc
                pygame.draw.arc( screen, wall_color[wall_i], [(j*tile_width) - (tile_width*0.4) - 2, (i*tile_height - (0.4*tile_height)), tile_width, tile_height], 3*PI/2, 0, 3 )
            if lvl[i][j] == 9:                  ## Drawing the exit gate
                pygame.draw.line( screen, white, ( (j*tile_width), (i*tile_height + (0.5*tile_height)) ), 
                                                ( (j*tile_width + tile_width), (i*tile_height + (0.5*tile_height)) ), 3)

def draw_player():
    pass

gameState = True
while gameState:
    timer.tick(fps)
    screen.fill(black)
    draw_board(level)
    draw_player()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameState = False
    
    pygame.display.flip()

pygame.quit()
