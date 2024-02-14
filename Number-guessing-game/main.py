import random
from art import logo
print(logo)
print("Welcome to the Number Guessing Game!")
print("i am thinking of a number between 1 and 100 ")
random_number=random.choice(range(1,100))
print(f"Psst, the correct answer is {random_number}")
Game_level=input("Choose difficulity level. Type 'easy' or 'hard':  ")
if Game_level=="easy":
    for i in reversed(range(1,11)):
        print(f"You have {i} attempts remaining to guess the number.")
        number_guess = int(input("Make a guess:"))
        if number_guess == random_number:
            print(f"You got it! the answer was {number_guess}")
            break
        elif number_guess > random_number:
            if i==1:
                print("Too high.\nYou have run out of guessess, you lose.")
            else:
                print("Too high.\nGuess again")
        else:
            if i==1:
                print("Too low.\n You have run out of guesses, you lose.")
            else:
                print("Too low.\nGuess again")
elif Game_level=="hard":
    for i in reversed(range(1,6)):
        print(f"you have {i} attempts remaining to guess the number.")
        number_guess = int(input("Make a guess:"))
        if number_guess == random_number:
            print(f"You got it!, the answer was {number_guess}")
            break
        elif number_guess > random_number:
            if i==1:
                print("Too high.\nYou have run out of guesses, you lose.")
            else:
                print("Too high.\nGuess again ")
        else:
            if i==1:
                print("Too low.\nYou have run out of guesses, you lose." )
            else:
                print("Too low.\nGuess again")
else:
    print("Invalid Choice\nGood By")
