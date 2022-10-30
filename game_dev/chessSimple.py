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
pygame.display.set_caption('Chessboard') ## Title of the game