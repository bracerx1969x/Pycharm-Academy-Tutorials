# Coffee Machine - Tutorial Python learning project
# from: https://hyperskill.org/projects/68?track=2
#
# This file contains my solutions for Stages #1 - 3 of this project

# Stage #1
# print("Starting to make a coffee")
# print("Grinding coffee beans")
# print("Boiling water")
# print("Mixing boiled water with crushed coffee beans")
# print("Pouring coffee into the cup")
# print("Pouring some milk into the cup")
# print("Coffee is ready!")

# --------dir
# Stage #2 & 3
water_per_cup = 200        # ml
milk_per_cup = 50          # ml
coffee_beans_per_cup = 15  # grams

avail_water = int(input("Write how many ml of water the coffee machine has:"))
avail_milk = int(input("Write how many ml of milk the coffee machine has:"))
avail_beans = int(input("Write how many grams of coffee beans the coffee machine has:"))
requested_coffee_cups = int(input("Write how many cups of coffee you will need:"))

# calculate needed ingredients
needed_water = water_per_cup * requested_coffee_cups
needed_milk = milk_per_cup * requested_coffee_cups
needed_beans = coffee_beans_per_cup * requested_coffee_cups

# calculate number of cups that can be made with available resources (Stage #3)
cups_water = avail_water // water_per_cup
cups_milk = avail_milk // milk_per_cup
cups_beans = avail_beans // coffee_beans_per_cup
max_cups_makeable = min((cups_water,cups_milk, cups_beans))

# Stage# 3 printout
# print(f"For {requested_coffee_cups} cups of coffee you will need:")
# print(f"{needed_water} ml of water")
# print(f"{needed_milk} ml of milk")
# print(f"{needed_beans} g of coffee beans")

# --------
# Stage #3 printout
if max_cups_makeable == requested_coffee_cups:
    print("Yes, I can make that amount of coffee")
elif max_cups_makeable > requested_coffee_cups:
    print("Yes, I can make that amount of coffee")
    print(f"(and even {max_cups_makeable - requested_coffee_cups} more than that")
else:
    print(f"No, I can make only {max_cups_makeable} cups of coffee")
