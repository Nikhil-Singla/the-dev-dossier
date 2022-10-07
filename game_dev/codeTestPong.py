import turtle as t
from random import randint
## import time
window = t.Screen()
window.title("Pong Practice")
window.bgcolor("black")
window.setup(width=800, height=600)
window.tracer(0) ## Stops window from updating

def dec():
    global scoreA
    scoreA = 0
    global scoreB
    scoreB = 0

# Pen
pen = t.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 230)
pen.write("Player A: 0     Player B: 0", align = "center", font=("Comic-Sans", 24, "normal"))

#A Bar
padA = t.Turtle() ## Create Turtle Item
padA.speed(0) ## Speed of the object
padA.shape("square")
padA.color("red")
padA.shapesize(stretch_wid=4, stretch_len=1) ## Multiple the dimensions to strech
padA.penup() ## Prevent drawing while the object is being moved
padA.goto(-375, 0) ## Move the object to this point at the start of the game.

#B Bar
padB = t.Turtle() 
padB.speed(0)
padB.shape("square")
padB.color("red")
padB.shapesize(stretch_wid=4, stretch_len=1)
padB.penup()
padB.goto(375, 0) ## Start object to the other side of Paddle A

#Ball
ball = t.Turtle() ## Ball Object
ball.speed(0)
ball.shape("circle") ## Different Ball Shape
ball.color("blue")
ball.penup()
ball.goto(0, 0)
ball.dx = 2.5
ball.dy = 2.5 ## Testing Change (Might edit, Default = 2)

#Function 
def padA_up():
    y = padA.ycor() ## Getting the y coordinate of turtle object
    if y >= 250: ## The paddle has center of 40 pixels and window size is 300 pixels either direction
        return
    y += 20 ## Add 20 pixels to y
    padA.sety(y) ## Sets the y coordinate to 20 above

def padA_down():
    y = padA.ycor() ## Getting the y coordinate of turtle object
    if y <= -250: ## The paddle has center of 40 pixels and window size is 300 pixels either direction
        return
    y -= 20 ## Removes 20 pixels to y
    padA.sety(y) ## Sets the y coordinate to 20 below

def padB_up():
    y = padB.ycor() ## Getting the y coordinate of turtle object
    if y >= 250: ## The paddle has center of 40 pixels and window size is 300 pixels either direction
        return
    y += 20 ## Add 20 pixels to y
    padB.sety(y) ## Sets the y coordinate to 20 below

def padB_down():
    y = padB.ycor() ## Getting the y coordinate of turtle object
    if y <= -250: ## The paddle has center of 40 pixels and window size is 300 pixels either direction
        return
    y -= 20 ## Removes 20 pixels to y
    padB.sety(y) ## Sets the y coordinate to 20 below

def ball_move():
    if ball.ycor() > 285: ## Boundary Check
        ball.sety(285) ## Ball Correction ## Note: Don't make the mistake of ".ycor =" and "sety()"
        ball.dy *= -1 ## Reverse Ball Speed
    if ball.ycor() < -285: ## Bottom Correction
        ball.sety(-285)
        ball.dy *= -1
        
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

def win_check():
    global scoreA 
    global scoreB
    if ball.xcor() > 385:
        ball.goto(randint(-50, 50), randint(-200, 200))
        ball.dx *= -1
        pen.clear() 
        scoreA += 1 
        pen.write("Player A: {}     Player B: {}".format(scoreA, scoreB), align = "center", font=("Comic-Sans", 24, "normal"))
    if ball.xcor() < -385:
        ball.goto(randint(-50, 50), randint(-200, 200))
        ball.dx *= -1
        scoreB += 1
        pen.clear()
        pen.write("Player A: {}     Player B: {}".format(scoreA, scoreB), align = "center", font=("Comic-Sans", 24, "normal"))

def check_col():
    if ((ball.xcor() > 350) and (ball.xcor() < 370) and (ball.ycor() > padB.ycor() - 43) and (ball.ycor() < padB.ycor()+43)): ## Tried using range function here, did not work out lol
        ball.dx *= -1
        ball.setx(ball.xcor() + ball.dx - 3)
    if ((ball.xcor() < -350) and (ball.xcor() > -370) and (ball.ycor() > padA.ycor() - 43) and (ball.ycor() < padA.ycor()+43)):
        ball.dx *= -1 ## Change the direction of ball
        ball.setx(ball.xcor() + ball.dx + 3)

##def Shoot():
  ##  bullet = t.Turtle()
  ##  x = padA.xcor()
  ##  x += 20
  ##  y = padA.ycor()
  ##  y += 20
  ##  bullet.speed(2)
  ##  bullet.shape("circle")
  ##  bullet.color("white")
  ##  bullet.penup()
  ##  bullet.goto(x,y)
## Will define this later when doing own update

#Keybinding
window.listen()
window.onkeypress(padA_up, "w")
window.onkeypress(padA_down, "s")
window.onkeypress(padB_up, "Up")
window.onkeypress(padB_down, "Down")

#Main game loop
def game():
    window.update()
    ball_move()
    win_check()
    check_col()

dec()
while True:
    ## start = time.time()
    t.ontimer(game(),1)
    ## end = time.time()
    ## tyme = end - start
    ## print(tyme)
    ## time.sleep(min(abs(0.02-tyme), 0.02))