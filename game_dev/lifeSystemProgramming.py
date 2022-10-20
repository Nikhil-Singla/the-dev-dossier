## Simulate life processes.
import pygame, random
from math import sqrt 

pygame.init() ## Initializing Game

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

## Screen dimensions
length = 300 
breadth = 300
## Screen dimensions end

screen = pygame.display.set_mode([length, breadth]) ## Resolution
pygame.display.set_caption('Particle Simulator')    ## Title of the game
background = black                                  ## Variable that can be edited later
frameRate = 60                                      ## Framerate 
font = pygame.font.Font('freesansbold.ttf', 16)     ## Font
timer = pygame.time.Clock()                         ## Help run our game at 60 FPS

list_P = []                 ## Empty array to store particles
pushRadius = 30             ## Radius for mouse pushing
particleCap = 100           ## Max Particles
sizeCircle = 2              ## Size of the particles
g = 0.0002                  ## Designated automatic gravity

class funcTimer():
    def __init__(self):
        self.start = pygame.time.get_ticks()    ## Clock starting

    def run(self, time):
        self.cooldown = time                    ## Set cooldown = Time (miliseconds)
        now = pygame.time.get_ticks()           ## Get current time
        if now - self.start >= self.cooldown:   ## If current time passed is greater than cooldown
            self.start = now                    ## Change current time
            return True                         ## Toggle Value of cooldown return 
        
class Particle():
    def __init__(self, color):
        self.x = random.randint(0, length)      ## X Cordinate randomization
        self.y = random.randint(0, breadth)     ## Y Cordinate randomization
        self.coords = [self.x, self.y]          ## Store coordinates in Tuple
        self.col = color                        ## Set color according to initialization

    def push(self, pos, radius = 30, g = 1):
        dx = self.x - pos[0]                ## Change in X between two points
        dy = self.y - pos[1]                ## Change in Y between two points
        dist = sqrt(dx*dx + dy*dy + 0.1)    ## Distance between particles, can never be 0
        dx /= dist                          ## Unit Vector Form of X Cordinate
        dy /= dist                          ## Unit Vector Form of Y Cordiate
        diff = radius - dist                ## Difference between 
        ## In Vector Theory, Finding v / |v| and then using this unit vector and adding it to base one.
        if diff > 0:
        ## Attraction Force with gravity when g > 0
            self.x -= diff*dx*g
            self.y -= diff*dy*g
        ## Repulsion Force with gravity when g < 0

    def centralize(self):
        self.push([int(length/2), int(breadth/2)], max(length, breadth), 0.02)

## Reference Move Function Code
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
## End Reference

def create(number, color):
    particles = []
    for i in range(0, number):                      ## Loop to create "number" of particles
        col = random.randint(0, 100)%len(color)     ## Get a random color from input list of colors
        particles.append(Particle(color[col]))      ## Add particles created to list
    return particles

## Own code
def move(list):
    global g
    for i in range(len(list)):
        for j in range(len(list)):
            list[i].push(list[j].coords, max(length, breadth), g)

moveFunc = False
gameState = True        ## Game Running
screen.fill(background) ## Have our initial background on the screen

runTimer = funcTimer()

while gameState:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: ## Different from quit(). Here, its an event
            gameState = False
        elif event.type == pygame.KEYDOWN:      ## If a key is pressed
            if event.key == pygame.K_ESCAPE:    ## If its the escape key
                gameState = False
            if event.key == pygame.K_r: ## If its the R key
                screen.fill(background) ## Wipe the screen
                list_P.clear()          ## Empty out the points list
                moveFunc = False        ## Future implementation of auto moving partciiles
            if event.key == pygame.K_s: ## If Key is "S"
                moveFunc = not moveFunc             ## Start the move function simulation
            if event.key == pygame.K_c:
                screen.fill(background)
                for p in list_P:
                    p.centralize()
    
        elif event.type == pygame.MOUSEBUTTONUP:    ## IF clicked
            pos = pygame.mouse.get_pos()            ## Get mouse position
            screen.fill(background)                 ## Reset print Screen
            for p in list_P:
                p.push(pos, pushRadius)             ## Update the points list with the new points away from mouse by a fixed radius
                pygame.draw.circle(screen, p.col, (p.x, p.y), sizeCircle) ## Draw the new points
  
    if len(list_P) < particleCap: ## Max Cap on particle count
        list_P += create(int(particleCap/10), [yellow, aqua])

    if moveFunc == True:
        if(runTimer.run(50)):
            move(list_P)
            screen.fill(background)
            for particle in list_P:
                pygame.draw.circle(screen, particle.col, (particle.x, particle.y), sizeCircle) ## Drawing board of particles per frame
    else:
        for particle in list_P:
            pygame.draw.circle(screen, particle.col, (particle.x, particle.y), sizeCircle) ## Drawing board of particles per frame

    #for particle in list_P:
            #move(list_P, list_P, 0.1)
            #pygame.draw.circle(screen, particle.col, (particle.x, particle.y), sizeCircle)

    pygame.display.flip() ## Update the content of the entire display   
    timer.tick(frameRate) ## Tick at the specified framerate
    

pygame.quit()