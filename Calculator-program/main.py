# def format_name(f_name,l_name):
#     title_name_f=f_name.title()
#     tile_name_l=l_name.title()
#     return f"{title_name_f} {tile_name_l}"
# title_name_is=format_name(f_name="angela",l_name="shahzad")
# print(title_name_is)
'''
practising the return as function output:
how to call one function from other function
'''

# def is_leap(year):
#     if year % 4 == 0:
#         if year % 100 == 0:
#             if year % 400 == 0:
#                 return "True"
#             else:
#                 return "False"
#         else:
#             return "True"
#     else:
#         return "False"
#
# # TODO: Add more code here 👇
# def days_in_month(year, month):
#     month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
#     leap_year_checker=is_leap(year)
#     if  leap_year_checker=="True":
#         if month-1 == 1:
#             return month_days[1]+1
#         else:
#             return month_days[month-1]
#     else:
#         return month_days[month-1]
# # 🚨 Do NOT change any of the code below
# year = int(input())  # Enter a year
# month = int(input())  # Enter a month
# days = days_in_month(year, month)
# print(days)
# def outer_function(a, b):
#     def inner_function(c, d):
#         return c + d
#     return inner_function(a, b)
# result = outer_function(5, 10)
# print(result)
# def my_function(a):
#     if a < 40:
#         return
#         print("Terrible")
#     if a < 80:
#         return "Pass"
#     else:
#         return "Great"
# print(my_function(25))
'''
Building a calculator
'''
def add(n1,n2):
    """this function return the sum of two numbers"""
    return n1+n2
def substract(n1,n2):
    """this function return the substraction of two numbers"""
    return n1-n2
def multiply(n1,n2):
    """this function return the multiply of two numbers"""
    return n1*n2
def divide(n1,n2):
    """this function return the division of two numbers"""
    return n1/n2

operations={"+":add,
            "-":substract,
            "*":multiply,
            "/":divide
}
from art import logo
def calculator():
    print(logo)
    num1 = float(input("What's the first number?: "))
    for symbols in operations.keys():
        print(symbols)
    operation_symbols = input("pick an operation in line above: ")
    num2 = float(input("What's the second number?: "))
    answer_first = operations[operation_symbols](num1, num2)
    print(f"{num1}{operation_symbols}{num2}={answer_first}")
    user_input = "y"
    while user_input == "y":
        user_input = input(f"Type 'y' to continue calculating with {answer_first}, or type 'n' to exit or type 'r' to restart: ")
        if user_input == "y":
            operation_symbols = input("Pick an operation above: ")
            num3 = float(input("What's the next number: "))
            answer_second = operations[operation_symbols](answer_first, num3)
            print(f"{answer_first}{operation_symbols}{num3}={answer_second}")
            answer_first = answer_second
        elif user_input=="r":
            user_input=="n"
            calculator()
        else:
            user_input = "n"
calculator()