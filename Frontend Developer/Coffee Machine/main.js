const input = require('sync-input')

class CoffeeMachine{
    constructor(water, milk, coffee, cups, money) {
        this.water = water;
        this.milk = milk;
        this.coffee = coffee;
        this.cups = cups;
        this.money = money;
        this.coffeeTypes = [
            {
                water : 250,
                milk: 0,
                coffee: 16,
                money: 4
            },
            {
                water : 350,
                milk: 75,
                coffee: 20,
                money: 7
            },
            {
                water : 200,
                milk: 100,
                coffee: 12,
                money: 6
            }
        ]
    }

    show_state(){
        console.log(`The coffee machine has:
${this.water} ml of water
${this.milk} ml of milk
${this.coffee} g of coffee beans
${this.cups} disposable cups
$${this.money} of money\n`)
    }

    buy(){
        let choice = input('What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino:\n')
        if (choice === 'back'){
            return;
        }
        choice = Number(choice)
        if (this.coffeeTypes[choice - 1].water > this.water){
            console.log('Sorry, not enough water!')
            return
        }
        if (this.coffeeTypes[choice - 1].milk > this.milk){
            console.log('Sorry, not enough milk!')
            return
        }
        if (this.coffeeTypes[choice - 1].coffee > this.coffee){
            console.log('Sorry, not enough coffee!')
            return
        }
        if (this.coffeeTypes[choice - 1].cups === 0){
            console.log('Sorry, not enough cups!')
            return
        }
        this.water -= this.coffeeTypes[choice - 1].water;
        this.milk -= this.coffeeTypes[choice - 1].milk;
        this.coffee -= this.coffeeTypes[choice - 1].coffee;
        this.money += this.coffeeTypes[choice - 1].money;
        this.cups -= 1;
    }
    fill(){
        this.water += Number(input("Write how many ml of water you want to add:\n"))
        this.milk += Number(input("Write how many ml of water you want to add:\n"))
        this.coffee += Number(input("Write how many grams of coffee beans you want to add:\n"))
        this.cups += Number(input("Write how many disposable coffee cups you want to add:\n"))
    }
    take(){
        console.log("I gave you $550")
        this.money = 0;
    }

    start() {
        while (true) {
            let action = input('Write action (buy, fill, take):\n')
            switch (action){
                case 'buy':
                    this.buy();
                    break;
                case 'fill':
                    this.fill();
                    break;
                case 'take':
                    this.take();
                    break;
                case 'remaining':
                    this.show_state()
                    break;
                case 'exit':
                    return
            }
        }

    }
}



let coffeeMachine = new CoffeeMachine(400, 540, 120, 9, 550)
coffeeMachine.start()



