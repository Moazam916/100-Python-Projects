from turtle import Turtle, Screen
import random
colors=["red", "orange", "yellow", "green", "blue", "purple"]
y_cordinate = -230
all_turtles=[]
is_game_over=False
screen=Screen()
screen.setup(width=500, height=500)
user_guess=screen.textinput(title="Make your bet", prompt="Which turtle will win the race? Enter a color: ")
for color in colors:
    red_turtle = Turtle(shape="turtle")
    red_turtle.speed("fastest")
    red_turtle.color(color)
    red_turtle.penup()
    red_turtle.goto(x=-230, y=y_cordinate)
    y_cordinate += 90
    all_turtles.append(red_turtle)

if user_guess:
    is_game_over=True
while is_game_over:
    for turtle in all_turtles:
        if turtle.xcor() > 230:
            is_game_over=False
            winning_color=turtle.pencolor()
            if winning_color == user_guess:
                print(f"You have won! The {winning_color} turtle is the winner")
            else:
                print(f"You have lost! The {winning_color} turtle is the winner")
        random_distance = random.randint(0, 10)
        turtle.forward(random_distance)
screen.exitonclick()