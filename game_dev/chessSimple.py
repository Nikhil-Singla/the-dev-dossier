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

length = 700 
breadth = 700

## Global Variables

screen = pygame.display.set_mode([length, breadth]) ## Resolution
pygame.display.set_caption('Chessboard') ## Title of the game
background = black  ## Variable that can be edited later
frameRate = 60  ## Framerate 
font = pygame.font.Font('freesansbold.ttf', 16) ## Font
timer = pygame.time.Clock() ## Help run our game at 60 FPS
timer_interval = 1000 # 0.5 seconds
timer_event = pygame.USEREVENT + 1


