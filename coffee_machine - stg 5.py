# Coffee Machine - Tutorial Python learning project
# from: https://hyperskill.org/projects/68?track=2
#
# This file contains my solutions thru Stages #5 of this project

# program flow:
# 0) initialize variables
# 1) report current status
# 2) get task input ('buy', 'fill', 'take')
# 3) branch based on input
#   a) 'buy':
#       1) get coffee type input ('espresso', 'latte', 'cappuccino')
#       2) process coffee:
#           a) check for available supplies
#           b) reduce available supplies
#           c) collect money
#   b) 'fill':
#       1) get replenish qty inputs (water, milk, coffee, cups)
#   c) 'take'
#       1) report qty of money taken
# 4) report current status

# program code:
# initialize variables
avail_water = 400  # milliliters(ml) of water
avail_milk = 540  # milliliters(ml) of milk
avail_beans = 120  # grams of coffee beans
avail_cups = 9  # disposable cups
collected_money = 550  # $ money collected from customers

# coffee ingredients { coffee_type: (cost, water, milk, beans) }
#   coffee_type = (1 = espresso, 2 = latte, 3 = cappuccino)
coffee_ingredients = {1: (4, 250, 0, 16),
                      2: (7, 350, 75, 20),
                      3: (6, 200, 100, 12)
                      }

process_actions = ('buy', 'fill', 'take', 'remaining', 'exit')


# process functions
# report current status
def report_status():
    print("The coffee machine has:")
    print(avail_water, "of water")
    print(avail_milk, "of milk")
    print(avail_beans, "of coffee beans")
    print(avail_cups, "of disposable cups")
    print("$" + str(collected_money), "of money")
    print()


def get_action():
    print("Write action (buy, fill, take, remaining, exit):")
    action = input()
    print()
    return action


def check_supplies(coffee_selection):
    global avail_water, avail_milk, avail_beans, avail_cups

    # determine needed supplies
    needed_water = coffee_ingredients[coffee_selection][1]
    needed_milk = coffee_ingredients[coffee_selection][2]
    needed_beans = coffee_ingredients[coffee_selection][3]

    supplies_needed =""
    if avail_water < needed_water:  return 'water'
    elif avail_milk < needed_milk: return 'milk'
    elif avail_beans < needed_beans: return 'coffee beans'
    elif avail_cups < 1: return 'cups'
    else: return 'available'

    # supplies_needed = []
    # if avail_water < needed_water: supplies_needed.append('water')
    # if avail_milk < needed_milk: supplies_needed.append('milk')
    # if avail_beans < needed_beans: supplies_needed.append('coffee beans')
    # if avail_cups < 1: supplies_needed.append('cups')
    #
    # # check if available supplies meet needs
    # return supplies_needed


def make_coffee(coffee_selection):
    global collected_money, avail_water, avail_milk, avail_beans, avail_cups
    supplies_needed = check_supplies(coffee_selection)
    if supplies_needed == 'available':
        print("I have enough resources, making you a coffee!")
        # collect money & deduct supplies
        collected_money += coffee_ingredients[coffee_selection][0]
        avail_water -= coffee_ingredients[coffee_selection][1]
        avail_milk -= coffee_ingredients[coffee_selection][2]
        avail_beans -= coffee_ingredients[coffee_selection][3]
        avail_cups -= 1
    else:
         print("Sorry, not enough", supplies_needed + "!")


def buy_coffee():
    print('What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:')
    coffee_choice = input()
    if coffee_choice != 'back':
        make_coffee(int(coffee_choice))
        print()

def replenish_supplies():
    global avail_water, avail_milk, avail_beans, avail_cups

    # replenish supplies
    print('Write how many ml of water do you want to add:')
    avail_water += int(input())
    print('Write how many ml of milk do you want to add:')
    avail_milk += int(input())
    print('Write how many grams of coffee beans do you want to add:')
    avail_beans += int(input())
    print('Write how many disposable cups of coffee do you want to add:')
    avail_cups += int(input())
    print()


def take_money():
    global collected_money
    print('I gave you $' + str(collected_money))
    print()
    collected_money = 0


# main program
current_action = get_action()
while current_action != 'exit':
    if current_action == 'buy':
        buy_coffee()
    elif current_action == 'fill':
        replenish_supplies()
    elif current_action == 'take':
        take_money()
    elif current_action == 'remaining':
        report_status()
    current_action = get_action()
