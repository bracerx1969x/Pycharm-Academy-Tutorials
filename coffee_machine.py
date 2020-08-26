# state constants
MAIN_MENU = 'main'
BACK = 'back'
BUY_COFFEE = 'buy'
TAKE_MONEY = 'take'
FILL_SUPPLIES = 'fill'
REPORT_STATUS = 'remaining'
SHUTDOWN = 'exit'
YES, NO = 'y', 'n'

# coffee machine constants
ESPRESSO, LATTE, CAPPUCCINO = '1', '2', '3'
WATER, MILK, COFFEE_BEANS, CUPS, MONEY = 'water', 'milk', 'coffee beans', 'disposable cups', 'money'
COFFEE_RESOURCES = (WATER, MILK, COFFEE_BEANS,)
RESOURCE_AMOUNT, RESOURCE_UOM = 0, 1
CUP_SUPPLIES = (CUPS,)
CASH_REGISTER = (MONEY,)
ALL_RESOURCES = COFFEE_RESOURCES + CUP_SUPPLIES + CASH_REGISTER


class StateError(Exception):

    def __init__(self, *args):
        if args:
            self.error_state = args[0]
            self.error_prompt = args[1]
            self.error_response = args[2]
        else:
            self.error_state = None
            self.error_prompt = None
            self.error_response = None

    def __str__(self):
        if self.error_state is not None:
            return f'State Error: State = {self.error_state}\n    \
            prompt = {self.error_prompt}, response = {self.error_response}'
        return None


class State:
    def __init__(self, fsm):
        self.fsm = fsm
        self.message = None

    def execute(self, response) -> object:
        if response is None:
            pass  # None response is a call request for a prompt, return prompt message
        else:
            self.message = response  # process response for action
        return self.message


class MainMenu(State):
    PROMPTS = ('\nWrite action (buy, fill, take, remaining, exit):',)
    VALID_INPUT = (BUY_COFFEE, FILL_SUPPLIES, TAKE_MONEY, REPORT_STATUS, SHUTDOWN,)

    def __init__(self, fsm):
        super().__init__(fsm)
        self.message = MainMenu.PROMPTS[0]

    def execute(self, response) -> object:
        if response is None:
            return self.message

        if response in MainMenu.VALID_INPUT:
            self.fsm.request_state(response)
        else:
            raise StateError('MainMenu()', self.message, response)
        return self.message


class BuyCoffee(State):
    PROMPTS = ('\nWhat do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:',)
    VALID_INPUT = (ESPRESSO, LATTE, CAPPUCCINO, BACK,)

    def __init__(self, fsm):
        super().__init__(fsm)
        self.coffee_maker = self.fsm.coffee_maker
        self.prompt = BuyCoffee.PROMPTS[0]
        self.message = None

    def execute(self, response) -> object:
        if response is None:
            return self.prompt

        if response in BuyCoffee.VALID_INPUT:
            if response != BACK:
                self.fsm.coffee_maker.brew_coffee(response)
            self.fsm.request_state(MAIN_MENU)  # return to main menu when complete
        else:
            raise StateError('BuyCoffee()', self.message, response)
        return None


class FillSupplies(State):

    PROMPTS = ('\nWrite how many ml of water do you want to add:',
               'Write how many ml of milk do you want to add:',
               'Write how many grams of coffee beans do you want to add:',
               'Write how many disposable cups of coffee do you want to add:',)

    __RESOURCE_ORDER = (WATER, MILK, COFFEE_BEANS, CUPS,)

    def __init__(self, fsm):
        super().__init__(fsm)
        self.__resource_index = 0
        self.message = None
        self.number_of_resources = len(FillSupplies.__RESOURCE_ORDER)
        self.prompt_gen = None
        self.prompt_gen = FillSupplies.PromptGen()
        self.counter = 0

    @staticmethod
    def PromptGen():
        indx = 0
        while indx < len(FillSupplies.PROMPTS):
            next_prompt = FillSupplies.PROMPTS[indx]
            yield indx, next_prompt
            indx += 1

    def execute(self, response) -> object:

        try:
            if response is not None:
                if str.isdigit(response):
                    self.fsm.coffee_maker.adjust_quantity(FillSupplies.__RESOURCE_ORDER[self.__resource_index],
                                                          int(response))
                else:
                    raise StateError('FillSupplies()', 'Response must be numbers only:', response)
            self.__resource_index, self.message = next(self.prompt_gen)
        except StopIteration:
            self.fsm.request_state(MAIN_MENU)  # return to main menu when complete
            self.__resource_index = 0  # make sure that resource index resets for next 'fill' call
            self.prompt_gen = FillSupplies.PromptGen()

        return self.message


class TakeMoney(State):

    def __init__(self, fsm):
        super().__init__(fsm)
        self.message = None

    def execute(self, response) -> object:
        self.fsm.coffee_maker.take_money()
        self.fsm.request_state(MAIN_MENU)  # return to main menu when complete
        return self.message


class ReportStatus(State):

    def __init__(self, fsm):
        super().__init__(fsm)
        self.message = None

    def execute(self, response) -> object:
        self.fsm.coffee_maker.supply_status()
        self.fsm.request_state(MAIN_MENU)  # return to main menu when complete
        return self.message


class Shutdown(State):

    def __init__(self, fsm):
        super().__init__(fsm)
        self.message = None

    def execute(self, response) -> object:
        self.fsm.coffee_maker.running = False
        return self.message


class FSMachine:

    def __init__(self, coffee_machine):
        self.coffee_maker = coffee_machine
        self._states = {MAIN_MENU:     MainMenu(self),
                        BUY_COFFEE:    BuyCoffee(self),
                        FILL_SUPPLIES: FillSupplies(self),
                        TAKE_MONEY:    TakeMoney(self),
                        REPORT_STATUS: ReportStatus(self),
                        SHUTDOWN:      Shutdown(self)
                        }
        self._current_state = self._states[MAIN_MENU]
        self.trigger_state = None

    def execute(self, response) -> object:
        message = self._current_state.execute(response)

        # if current state triggers a state change, execute the new state
        while self.trigger_state is not None:
            self._change_state(self.trigger_state)
            self.trigger_state = None
            message = self._current_state.execute(None)

        return message

    def request_state(self, to_state):
        """ States will call this method to request a change """
        if to_state in self._states.keys():
            self.trigger_state = to_state
        else:
            self.trigger_state = None

    def _change_state(self, to_state):
        """ FSMachine performs the actual state change here """
        if to_state in self._states.keys():
            self._current_state = self._states[to_state]
        else:
            raise Exception(f'FSM error: Invalid state ="{to_state}"')


class CoffeeMachine:

    def __init__(self, resource_list, coffee_list: dict, cash_register):
        self.fsm = FSMachine(self)
        self.running = True
        self.request = None
        self.resource_list = resource_list
        self.coffee_list = coffee_list
        self.cash_register = cash_register

    def run(self):
        """Runs the CoffeeMachine once it is created"""
        self.request = None
        response = self.fsm.execute(self.request)
        while self.running:
            print(response)
            self.request = input()
            response = self.fsm.execute(self.request)

    # The remainder of the the CoffeeMachine functions
    # are only called through the States to control the actions, not directly
    def get_quantity(self, resource) -> int:
        """Gets the available amount of the specified resource"""
        if resource in self.resource_list.keys():
            return int(self.resource_list[resource][RESOURCE_AMOUNT])
        elif resource == MONEY:
            return int(self.cash_register[resource][RESOURCE_AMOUNT])
        else:
            return -1  # should never return this unless asking for an invalid resource, returns -1 to catch errors

    def adjust_quantity(self, resource, amount):
        """ adjust resource amount, positive to add & negative subtracts """

        if resource == MONEY:
            self.cash_register[resource][RESOURCE_AMOUNT] += amount
        elif resource in self.resource_list.keys():
            self.resource_list[resource][RESOURCE_AMOUNT] += amount
        else:
            print('-1')  # should never print this unless asking for an invalid resource, prints '-1' to catch errors

    def are_supplies_available(self, coffee_type) -> (bool, str):

        for each_ingredient, amount_needed in self.coffee_list[coffee_type].items():
            if each_ingredient in COFFEE_RESOURCES and amount_needed > self.get_quantity(each_ingredient):
                return False, each_ingredient
        # check disposable cup supply too
        if self.get_quantity(CUPS) < 1:
            return False, CUPS
        else:
            return True, None

    def supply_status(self):
        _RESOURCE_ORDER = ALL_RESOURCES
        print()
        print('The coffee machine has:')
        for resource in _RESOURCE_ORDER:
            print(
                    f'{"$" if resource == MONEY else ""}{self.get_quantity(resource)} of {resource}')

    def get_cost(self, coffee_type):
        return self.coffee_list[coffee_type][MONEY]

    def brew_coffee(self, coffee_type):
        """ brews coffee after checking for needed supplies, then deducts supplies and collects money """
        supplies_available, needed_supply = self.are_supplies_available(coffee_type)
        if supplies_available:
            print('I have enough resources, making you a coffee!')
            # deduct supplies & collect money for coffee
            self.deduct_resources(coffee_type)
            self.collect_money(self.get_cost(coffee_type))
        else:
            print(f'Sorry, not enough {needed_supply}!')

    def deduct_resources(self, coffee_type):
        """ reduces inventory per coffee made """
        for each_ingredient, amount_needed in self.coffee_list[coffee_type].items():
            if each_ingredient in COFFEE_RESOURCES:  # necessary to only allow ingredients to be adjusted (not MONEY)
                self.adjust_quantity(each_ingredient, -amount_needed)

        # reduce disposable cup supply too
        self.adjust_quantity(CUPS, -1)

    def collect_money(self, amount):
        """ use this in brew_coffee to collect money from customer """
        self.adjust_quantity(MONEY, amount)

    def take_money(self):
        """ used by TakeMoney state to remove money from the coffee maker's cash register """
        amount_taken = self.get_quantity(MONEY)
        print(f'I gave you ${amount_taken}')
        self.adjust_quantity(MONEY, -amount_taken)


if __name__ == '__main__':
    # coffee_resources = {ingredient: [RESOURCE_AMOUNT: quantity, RESOURCE_UOM: measurement unit], ...}
    coffee_resources = {WATER:        [400, 'ml'],
                        MILK:         [540, 'ml'],
                        COFFEE_BEANS: [120, 'grams'],
                        CUPS: [9, '']}
    starting_money = {MONEY: [550, '$']}
    # coffee_list = {coffee type: {cost, water needed, milk needed, beans needed}}
    coffee_options = {ESPRESSO:   {MONEY: 4, WATER: 250, MILK: 0, COFFEE_BEANS: 16},
                      LATTE:      {MONEY: 7, WATER: 350, MILK: 75, COFFEE_BEANS: 20},
                      CAPPUCCINO: {MONEY: 6, WATER: 200, MILK: 100, COFFEE_BEANS: 12}
                      }
    coffee_maker = CoffeeMachine(coffee_resources, coffee_options, starting_money)
    coffee_maker.run()
