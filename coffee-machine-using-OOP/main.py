from menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine
coffee_machine_start = True
coffee_menu = Menu()
resources_sufficient = CoffeeMaker()
my_money_machine = MoneyMachine()
available_option = coffee_menu.get_items()
while coffee_machine_start:
    coffee_input = input(f"What would you like {available_option}?: ")
    if coffee_input == "espresso" or coffee_input == "latte" or coffee_input == "cappuccino":
        finding_drink = coffee_menu.find_drink(order_name=coffee_input)
        resources_sufficient_for_order = resources_sufficient.is_resource_sufficient(drink=finding_drink)
        if resources_sufficient_for_order:
            process_coins = my_money_machine.make_payment(cost=finding_drink.cost)
            if process_coins:
                resources_sufficient.make_coffee(order=finding_drink)
    elif coffee_input == "report":
        report_resources = resources_sufficient.report()
        money_report = my_money_machine.report()
    elif coffee_input == "off":
        coffee_machine_start = False
        print("Turning off machines, Please comeback")