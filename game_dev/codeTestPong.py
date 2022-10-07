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
padA.goto(-375, 0) ## move the object to this point at the start of the game.

#B Bar
padB = t.Turtle()
padB.speed(0)
padB.shape("square")
padB.color("red")
padB.shapesize(stretch_wid=4, stretch_len=1)
padB.penup()
padB.goto(375, 0)

#Ball
ball = t.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("blue")
ball.penup()
ball.goto(0, 0)

#Function 
def Shoot():
    bullet = t.Turtle()
    x = padA.xcor()
    x += 20
    y = padA.ycor()
    y += 20
    bullet.speed(2)
    bullet.shape("circle")
    bullet.color("white")
    bullet.penup()
    bullet.goto(x,y)


#Keybinding
window.listen()
window.onkeypress(Shoot,"space")

#Main game loop
while True:
    window.update()
