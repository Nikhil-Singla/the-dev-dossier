import turtle as t

window = t.Screen()
window.title("Pong Practice")
window.bgcolor("black")
window.setup(width=800, height=600)
window.tracer(0) ## Stops window from updating

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
ball.dx = 2
ball.dy = 2 ## Testing Change (Might edit, Default = 2)

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
    ball.setx(ball.xcor() + 0.05*ball.dx)
    ball.sety(ball.ycor() + 0.05*ball.dy)

def win_check():
    if ball.xcor() > 385:
        ball.goto(0, 0)
        ball.dx = -1
    if ball.xcor() < -385:
        ball.goto(0, 0)
        ball.dx = 1

window.listen()
window.onkeypress(padA_up, "w")
window.onkeypress(padA_down, "s")
window.onkeypress(padB_up, "Up")
window.onkeypress(padB_down, "Down")

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

#Main game loop
while True:
    window.update()
    ball_move()
    win_check()