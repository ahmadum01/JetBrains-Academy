class Coffee:
    def __init__(self, kind: 'espresso | latte | cappuccino'):
        self.water = {'espresso': 250, 'latte': 350, 'cappuccino': 200}.get(kind, 0)
        self.milk = {'espresso': 0, 'latte': 75, 'cappuccino': 100}.get(kind, 0)
        self.coffee = {'espresso': 16, 'latte': 20, 'cappuccino': 12}.get(kind, 0)
        self.cups = {'espresso': 1, 'latte': 1, 'cappuccino': 1}.get(kind, 0)
        self.money = {'espresso': 4, 'latte': 7, 'cappuccino': 6}.get(kind, 0)


class CoffeeMachine:
    def __init__(self, water, milk, coffee, cups, money):
        self.water = water
        self.milk = milk
        self.coffee = coffee
        self.cups = cups
        self.money = money

    def buy(self, kind):
        coffee = Coffee({'1': 'espresso', '2': 'latte', '3': 'cappuccino'}.get(kind, 0))
        match self.resources_is_enough(coffee):
            case command if 'I have enough' in command:
                print(command)
                self.water -= coffee.water
                self.milk -= coffee.milk
                self.coffee -= coffee.coffee
                self.cups -= coffee.cups
                self.money += coffee.money
            case command:
                print(command)

    def fill(self):
        self.water += int(input('Write how many ml of water you want to add:\n'))
        self.milk += int(input('Write how many ml of milk you want to add:\n'))
        self.coffee += int(input('Write how many grams of coffee beans you want to add:\n'))
        self.cups += int(input('Write how many disposable coffee cups you want to add:\n'))

    def take(self):
        print('I gave you ${self.money}')
        self.money = 0

    def resources_is_enough(self, coffee: Coffee):
        if self.water < coffee.water:
            return 'Sorry, not enough water!'
        if self.milk < coffee.milk:
            return 'Sorry, not enough milk!'
        if self.coffee < coffee.coffee:
            return 'Sorry, not enough coffee!'
        if self.cups < coffee.cups:
            return 'Sorry, not enough cups!'
        return 'I have enough resources, making you a coffee!!'

    def print(self):
        print('\nThe coffee machine has:', f'{self.water} of water', f'{self.milk} of milk',
              f'{self.coffee} of coffee beans', f'{self.cups} of disposable cups', f'{self.money} of money', sep='\n')

    def start(self):
        while True:
            match input('\nWrite action (buy, fill, take):\n'):
                case 'buy':
                    kind = input('What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino:\n')
                    if kind == 'back':
                        continue
                    self.buy(kind)
                case 'fill':
                    self.fill()
                case 'take':
                    self.take()
                case 'remaining':
                    self.print()
                case 'exit':
                    break


if __name__ == '__main__':
    coffee_machine = CoffeeMachine(400, 540, 120, 9, 550)
    coffee_machine.start()

