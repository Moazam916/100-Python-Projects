from art import logo, vs
from game_data import data
import os
import random
print(logo)
current_score=0
Game_over=True
def input_data():
    """Returning the random data for game"""
    return random.choice(data)
while Game_over == True:
    first_choice = input_data()
    second_choice = input_data()
    print(f"Compare A: {first_choice['name']}, {first_choice['description']}, from {first_choice['country']}")
    print(vs)
    print(f"Against B: {second_choice['name']}, {second_choice['description']}, from {second_choice['country']}")
    user_choice = input("Who has more followers? Type 'A' or 'B': ")
    if user_choice == "A" and first_choice['follower_count'] > second_choice['follower_count']:
        current_score += 1
        print(f"You are right! Current score is: {current_score}.")
    elif user_choice == "B" and second_choice['follower_count'] > first_choice['follower_count']:
        current_score += 1
        print(f"You are right! Current score is: {current_score}.")
    else:
        os.system('cls')
        print(logo)
        Game_over=False
        print(f"Sorry, that's wrong. Final score: {current_score}")