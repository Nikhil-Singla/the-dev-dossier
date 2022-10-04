import turtle as t

window = t.Screen()
window.title("Trial Game")
window.bgcolor("black")
window.setup(width=800, height=600)
window.tracer(0)

#A Bar
padA = t.Turtle()
padA.speed(0)
padA.shape("square")
padA.color("red")
padA.shapesize(stretch_wid=4, stretch_len=1)
padA.penup()
padA.goto(-375, 0)

#B Bar
padB = t.Turtle()
padB.speed(0)
padB.shape("square")
padB.color("red")
padB.shapesize(stretch_wid=4, stretch_len=1)
padB.penup()
padB.goto(375, 0)

#Main game loop
while True:
    window.update()
