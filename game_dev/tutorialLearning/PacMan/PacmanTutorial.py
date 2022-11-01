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

width = 900
height = 950

screen = pygame.display.set_mode([width, height])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)

gameState = True
while gameState:
    timer.tick(fps)
    screen.fill(black)

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameState = False
    
    pygame.display.flip()

pygame.quit()
