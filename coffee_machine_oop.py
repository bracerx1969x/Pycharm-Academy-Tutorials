class CoffeeMachine:

    __STATE_OPTIONS = ['MAIN', 'BUY', 'FILL', 'TAKE', 'REMAINING', 'EXIT']

    __MAIN_MENU = 'Write action (buy, fill, take, remaining, exit):'
    __COFFEE_SELECT = 'What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:'
    __FILL_REQUEST = ['Write how many ml of water do you want to add:',
                      'Write how many ml of milk do you want to add:,'
                      'Write how many grams of coffee beans do you want to add:',
                      'Write how many disposable cups of coffee do you want to add:']

    coffee_ingredients = {1: (4, 250, 0, 16),
                          2: (7, 350, 75, 20),
                          3: (6, 200, 100, 12)
                          }

    def __init__(self):
        self.avail_water = 400  # milliliters(ml) of water
        self.avail_milk = 540  # milliliters(ml) of milk
        self.avail_beans = 120  # grams of coffee beans
        self.avail_cups = 9  # disposable cups
        self.collected_money = 550  # $ money collected from customers
        self.display_menu('MAIN')   # MAIN menu to start

    def display_menu(self, state):  # change state & display menu
        if state == 'MAIN':
            self.__state = 'MAIN'
            print(self.__MAIN_MENU)
        elif state == 'BUY':
            self.__state = 'BUY'
            print(self.__COFFEE_SELECT)

    def process_input(self, action):
        if self.__state == 'MAIN':
            if action == 'buy':  # buy coffee options
                self.display_menu('BUY')

            elif action == 'fill':  # fill supplies
                pass

            elif action == 'take':  # take money
                pass

            elif action == 'remaining':  # report machine status
                self.report_status()
                self.display_menu('MAIN')

            elif action == 'exit':  # exit program
                global RUNNING
                RUNNING = False

        elif self.__state == 'BUY':  #  choose coffee flavor menu
            if action == '1' or action == '2' or action == '3':
                self.buy_coffee(int(action))
                self.display_menu('MAIN')

            else:  # action == 'back' or processed coffee, now back to main menu
                self.display_menu('MAIN')

    def check_supplies(self, coffee_selection):

        # determine needed supplies
        needed_water = self.coffee_ingredients[coffee_selection][1]
        needed_milk = self.coffee_ingredients[coffee_selection][2]
        needed_beans = self.coffee_ingredients[coffee_selection][3]

        supplies_needed = ""
        if self.avail_water < needed_water:
            return 'water'
        elif self.avail_milk < needed_milk:
            return 'milk'
        elif self.avail_beans < needed_beans:
            return 'coffee beans'
        elif self.avail_cups < 1:
            return 'cups'
        else:
            return 'available'

    def buy_coffee(self, coffee_selection):

        supplies_needed = self.check_supplies(coffee_selection)
        if supplies_needed == 'available':
            print("I have enough resources, making you a coffee!\n")
            # collect money & deduct supplies
            self.collected_money += self.coffee_ingredients[coffee_selection][0]
            self.avail_water -= self.coffee_ingredients[coffee_selection][1]
            self.avail_milk -= self.coffee_ingredients[coffee_selection][2]
            self.avail_beans -= self.coffee_ingredients[coffee_selection][3]
            self.avail_cups -= 1
        else:
            print("Sorry, not enough", supplies_needed + "!\n")

    def replenish_supplies(self):

        # replenish supplies
        # TODO remove inputs and set status to collect the data through main loop
        print('Write how many ml of water do you want to add:')
        self.avail_water += int(input())
        print('Write how many ml of milk do you want to add:')
        self.avail_milk += int(input())
        print('Write how many grams of coffee beans do you want to add:')
        self.avail_beans += int(input())
        print('Write how many disposable cups of coffee do you want to add:')
        self.avail_cups += int(input())
        print()

    # report current status
    def report_status(self):
        print("\nThe coffee machine has:")
        print(self.avail_water, "of water")
        print(self.avail_milk, "of milk")
        print(self.avail_beans, "of coffee beans")
        print(self.avail_cups, "of disposable cups")
        print("$" + str(self.collected_money), "of money\n")

    def print_state(self):
        print(self.__state)

# initialize coffee machine
coffee_machine = CoffeeMachine()

# main loop

RUNNING = True
while RUNNING:
    cm_action = input()
    coffee_machine.process_input(cm_action)
