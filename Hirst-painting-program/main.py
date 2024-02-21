import turtle as t
import random
timmy=t.Turtle()
t.colormode(255)
timmy.shape(name="arrow")
colors_list=[(177, 11, 33), (185, 169, 13), (185, 73, 25), (225, 243, 235), (245, 215, 78), (208, 160, 82), (172, 22, 15), (236, 242, 247)]
step_size=50
def making_circles_horizentally(y_cordinates):
    for step_size in range(0, 500, 50):
        timmy.goto(step_size,y_cordinates)
        timmy.hideturtle()
        timmy.color("white", random.choice(colors_list))
        timmy.begin_fill()
        timmy.pendown()
        timmy.circle(20)
        timmy.end_fill()
        timmy.penup()


def moving_turtle_vertically():
    for i in range(0,500, 50):
        making_circles_horizentally(y_cordinates=i)

timmy.speed('fastest')
moving_turtle_vertically()
print(timmy.pos())
screen=t.Screen()
screen.exitonclick()