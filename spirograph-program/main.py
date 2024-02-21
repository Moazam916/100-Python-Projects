import turtle as t
import random


timmy=t.Turtle()
t.colormode(255)
timmy.shape(name="arrow")
def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    my_tuple=(r, g, b)
    return my_tuple
def spirograpgh(step_size):
    timmy.speed("fastest")
    timmy.pensize(2)
    for i in range(0, int(360/step_size)):
        color=random_color()
        timmy.color(color[0], color[1], color[2])
        timmy.circle(100)
        #timmy.tilt(10)
        timmy.setheading(timmy.heading()+step_size)
spirograpgh(5)
screen=t.Screen()
screen.exitonclick()