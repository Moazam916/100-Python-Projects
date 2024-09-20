import turtle
import pandas

Correct_states = 0
game_is_on = True
guessed_state = []
undressed_states = []
data = pandas.read_csv("50_states.csv")
print(data)
all_states = data["state"].to_list()
screen = turtle.Screen()
image = "blank_states_img.gif"
screen = turtle.Screen()
screen.title("Welcome to US states game")
screen.addshape(image)
turtle.shape(image)
while game_is_on:
    if len(guessed_state) == 50:
        game_is_on = False
    user_answer = screen.textinput(title=f"{Correct_states}/50 States Correct",
                                   prompt="what is another state's name? ").title()
    print(user_answer)
    if user_answer == "Break" or user_answer == "Exit":
        undressed_states=[state for state in all_states if state not in guessed_state]
        df = pandas.DataFrame(undressed_states, columns=["States_Need_learn"])
        df.to_csv("states_need_to_learn.csv")
        print(df)
        break
    if user_answer in all_states:
        if user_answer not in guessed_state:
            new_turtle = turtle.Turtle()
            new_turtle.hideturtle()
            new_turtle.penup()
            data_match = data[data.state == user_answer]
            print(data_match)
            new_x = int(data_match.x.iloc[0])
            new_y = int(data_match.y.iloc[0])
            new_turtle.goto(x=new_x, y=new_y)
            print(f"{new_turtle.pos()}")
            new_turtle.write(arg=f"{user_answer}", align="center", font=('Arial', 8, 'normal'))
            Correct_states += 1
            guessed_state.append(user_answer)
    else:
        print("state is not in list")

