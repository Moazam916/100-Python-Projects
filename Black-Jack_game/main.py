############### Blackjack Project #####################

#Difficulty Normal 😎: Use all Hints below to complete the project.
#Difficulty Hard 🤔: Use only Hints 1, 2, 3 to complete the project.
#Difficulty Extra Hard 😭: Only use Hints 1 & 2 to complete the project.
#Difficulty Expert 🤯: Only use Hint 1 to complete the project.

############### Our Blackjack House Rules #####################

## The deck is unlimited in size.
## There are no jokers.
## The Jack/Queen/King all count as 10.
## The the Ace can count as 11 or 1.
## Use the following list as the deck of cards:
## cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
## The cards in the list have equal probability of being drawn.
## Cards are not removed from the deck as they are drawn.
## The computer is the dealer.

##################### Hints #####################
import random
import os
from art import logo
cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
your_cards=[]
computer_cards=[]
game_over="y"
user_input="y"
while game_over=="y":
    play_black_jack=input("Do you want to play Blacjack? tye 'y' or 'n': ")
    os.system('cls')
    if play_black_jack=="y":
        your_cards = []
        computer_cards = []
        user_input = "y"
        print(logo)
        for i in range(1, 3):
            your_cards.append(random.choice(cards))
            computer_cards.append(random.choice(cards))
        print(f"Your cards: {your_cards}, current score is: {sum(your_cards)}")
        print(f"Computer's first card: {computer_cards[0]}")
        while user_input == "y":
            user_input = str(input("Type 'y' to get another card, type 'n' to pass: "))
            if user_input == "y":
                your_cards.append(random.choice(cards))
                print(f"your cards: {your_cards}, final score is: {sum(your_cards)}")
                # print(f"Computer's card: {computer_cards}, computer score is {sum(computer_cards)}")
                if sum(your_cards) > 21:
                    print("you went over, you loose ")
                    user_input = "n"
                # elif sum(your_cards) == 21:
                #     if sum(computer_cards) == sum(your_cards):
                #         print("its draw")
                #     else:
                #         print("you win")
                # elif sum(your_cards) > sum(computer_cards):
                #     print("you win")
                # else:
                #     print("you lose")
            else:
                print(f"you cards: {your_cards}, final score is: {sum(your_cards)}")
                print(f"computer cards:{computer_cards}, computer's final score is: {sum(computer_cards)}")
                user_input = "n"
                if sum(your_cards) == sum(computer_cards):
                    print("its draw")
                elif sum(your_cards) > sum(computer_cards) and sum(your_cards) <= 21:
                    print("you win")
                elif sum(your_cards) < sum(computer_cards) and sum(computer_cards) <= 21:
                    print("you loose")
    else:
        game_over="n"
