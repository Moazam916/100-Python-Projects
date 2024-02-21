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

def go(heading, step_size):
    color=random_color()
    timmy.color(color[0], color[1], color[2])
    timmy.pensize(10)
    timmy.setheading(heading)
    timmy.forward(step_size)


def random_walk(step_size, steps):
    # Assumes turtle.mode('standard')
    DIRECTIONS = (EAST, NORTH, WEST, SOUTH) = (0, 90, 180, 270)
    for _ in range(steps):
        go(random.choice(DIRECTIONS), step_size)

random_walk(step_size=50, steps=100)
screen=t.Screen()
screen.exitonclick()