'''
How to build a silent auction program, where bidder can place his/her bid and program can determine highest bidders among the bidders.
This programe ask for input parameters such as name and price then if there is any other bidder it will clear console and then repeat the same process untill user say no other bidder.
Then it determins maximum value along with its bidder name
'''
import os
from art import logo
print(logo)
name=input("What is your name?")
price=int(input("what is your price?"))
bid={}
bid[f"{name}"]=price
other_bider="yes"
while other_bider=="yes":
    if input("If there are other bidder who want to bid type 'yes' or 'no' ") == "yes":
        os.system('cls')
        name = input("What is you name?")
        price = int(input("what is your price?"))
        bid[f"{name}"] = price
    else:
        other_bider="no"
        os.system('cls')
        max_bid=max(zip(bid.values(),bid.keys()))
        print(f"the winner is {max_bid[1]} with a bid of ${max_bid[0]}")