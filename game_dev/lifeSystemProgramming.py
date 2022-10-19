## Simulate life processes.

from dis import dis
import pygame, random
from math import sqrt 

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
yellow = (255,255,0)
## End Palette

screen = pygame.display.set_mode([500, 500]) ## Resolution
pygame.display.set_caption('Not Adventure Capitalist') ## Title of the game
background = black  ## Variable that can be edited later
frameRate = 60  ## Framerate 
font = pygame.font.Font('freesansbold.ttf', 16) ## Font
timer = pygame.time.Clock() ## Help run our game at 60 FPS

list_P = []
radius = 30
class Particle():
    def __init__(self, color):
        self.x = random.randint(0, 500)
        self.y = random.randint(0, 500)
        self.col = color


"""def move(particle1, particle2, g):
    for i in range(0, len(particle1)):
        fx = 0
        fy = 0
        for j in range(0, len(particle2)):
            a = particle1[i]
            b = particle2[j]
            dx = a.x - b.x
            dy = a.y - b.y
            dist = sqrt(dx*dx + dy*dy)
            if dist > 0:
                F = g * (1/dist)
                fx += (F*dx)
                fy += (F*dy)
            a.x += fx
            a.y += fy"""

def create(number, color):
    particles = []
    for i in range(0, number):
        col = random.randint(0, 100)%len(color)
        particles.append(Particle(color[col]))
    
    return particles

def push(pos, p, radius):
    dx = p.x - pos[0]
    dy = p.y - pos[1]
    dist = sqrt(dx*dx + dy*dy)
    dx /= dist
    dy /= dist
    diff = radius - dist
    ## Equation of line = y - p.y = slope*(x - p.x)
    if diff > 0:
        print(pos)
        p.x += diff*dx
        p.y += diff*dy
        

moveFunc = False
gameState = True ## Game Running
screen.fill(background) ## Have our initial background on the screen

while gameState:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: ## Different from quit(). Here, its an event
            gameState = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gameState = False
            if event.key == pygame.K_r:
                screen.fill(background)
                list_P.clear()
                moveFunc = False
            if event.key == pygame.K_s:
                moveFunc = True

        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos() 
            screen.fill(background)
            for p in list_P:
                push(pos, p, radius)
                pygame.draw.circle(screen, p.col, (p.x, p.y), 2)

    if len(list_P) < 1000: ## Max Cap on particle count
        list_P += create(200, [yellow, aqua])

    for particle in list_P:
            pygame.draw.circle(screen, particle.col, (particle.x, particle.y), 2)
##            if moveFunc == True:

    pygame.display.flip() ## Update the content of the entire display   
    timer.tick(frameRate) ## Tick at the specified framerate
    

pygame.quit()