from menu import MENU, resources
def adding_back_deducted_resources(coffee_input_from_user, enough_money):
    if enough_money=="Money Refunded":
        if coffee_input_from_user=="espresso":
            resources["water"] += 50
            resources["coffee"] += 18
        elif coffee_input_from_user=="latte":
            resources["water"] += 200
            resources["milk"] += 150
            resources["coffee"] += 24
        elif coffee_input_from_user=="cappuccino":
            resources["water"] += 250
            resources["milk"] += 100
            resources["coffee"] += 24
    else:
        print("Invalid responce from adding_back_deducted_resources function")


def checking_resources(coffee_input_from_user):
    if coffee_input_from_user=="espresso":
        if MENU[f"{coffee_input_from_user}"]["ingredients"]["water"] <= resources["water"] and MENU[f"{coffee_input_from_user}"]["ingredients"]["coffee"] <= resources["coffee"]:
            resources["water"] -= 50
            resources["coffee"] -= 18
            return "Sufficient_resources"
        else:
            return "Inufficient_resources"
    elif coffee_input_from_user=="latte":
        if MENU[f"{coffee_input_from_user}"]["ingredients"]["water"]<=resources["water"] and MENU[f"{coffee_input_from_user}"]["ingredients"]["milk"]<=resources["milk"] and MENU[f"{coffee_input_from_user}"]["ingredients"]["coffee"] <= resources["coffee"]:
            resources["water"] -= 200
            resources["milk"] -= 150
            resources["coffee"] -= 24
            return "Sufficient_resources"
        else:
            return "Inufficient_resources"
    elif coffee_input_from_user=="cappuccino":
        if MENU[f"{coffee_input_from_user}"]["ingredients"]["water"]<=resources["water"] and MENU[f"{coffee_input_from_user}"]["ingredients"]["milk"]<=resources["milk"] and MENU[f"{coffee_input_from_user}"]["ingredients"]["coffee"] <= resources["coffee"]:
            resources["water"] -= 250
            resources["milk"] -= 100
            resources["coffee"] -= 24
            return "Sufficient_resources"
        else:
            return "Inufficient_resources"
    else:
        print("invalid responce")


def money_transaction(coffee_input,quarters,dimes,nickles,pennies):
    total_cost=quarters*0.25+dimes*0.10+nickles*0.05+pennies*0.01
    if coffee_input=="espresso" and total_cost>=MENU["espresso"]["cost"]:
        change=total_cost-MENU["espresso"]["cost"]
        return True, change
    elif coffee_input=="latte" and total_cost>=MENU["latte"]["cost"]:
        change=total_cost-MENU["latte"]["cost"]
        return True, change
    elif coffee_input=="cappuccino" and total_cost>=MENU["cappuccino"]["cost"]:
        change=total_cost-MENU["cappuccino"]["cost"]
        return True, change
    else:
        return False, "Money Refunded"


def resources_report():
    return resources

Coffee_machine_start=True
while Coffee_machine_start==True:
    coffee_input = input("What would you like? (espresso/latte/cappuccino): ")
    if coffee_input == "espresso" or coffee_input == "latte" or coffee_input == "cappuccino":
        checking_for_resources = checking_resources(coffee_input_from_user=coffee_input)
        if checking_for_resources == "Sufficient_resources":
            print("please insert coins.")
            quarters = int(input("how many quarters?: "))
            dimes = int(input("how many dimes?: "))
            nickles = int(input("how many nickles?: "))
            pennies = int(input("how many pennies?: "))
            is_money_sufficient = money_transaction(coffee_input=coffee_input, quarters=quarters, dimes=dimes,
                                                    nickles=nickles, pennies=pennies)
            if is_money_sufficient[0] == True:
                print(f"Here is ${round(is_money_sufficient[1], 1)} in change")
                print(f"Here your {coffee_input} ☕, Enjoy")
            else:
                adding_back_deducted_resources(coffee_input_from_user=coffee_input, enough_money=is_money_sufficient[1])
                print(f"Sorry that's not enough money. {is_money_sufficient[1]}")
        else:
            print("Sorry, resources are not sufficient")
    elif coffee_input == "report":
        report = resources_report()
        print(report)
    elif coffee_input == "off":
        Coffee_machine_start = False
        print("Coffee machine is turning off, please comeback")
