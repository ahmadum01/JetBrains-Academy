let currencies = {
    'USD': 1,
    'JPY': 113.5,
    'EUR': 0.89,
    'RUB': 74.36,
    'GBP': 0.75
}
const input = require('sync-input');
console.log(`Welcome to Currency Converter!
1 USD equals  1 USD
1 USD equals  113.5 JPY
1 USD equals  0.89 EUR
1 USD equals  74.36 RUB
1 USD equals  0.75 GBP`)



while(true) {
    console.log(`What do you want to do?
1-Convert currencies 2-Exit program`)
    let option = input()
    if (option === '1') {
        console.log('What do you want to convert?')
        let from = input('From: ').toUpperCase()
        if (currencies.hasOwnProperty(from)) {
            let to = input('To: ').toUpperCase()
            if (currencies.hasOwnProperty(to)) {
                let amount = Number(input('Amount: '))
                if (amount < 1) {
                    console.log('The amount can not be less than 1')
                } else if (isNaN(amount)) {
                    console.log('The amount has to be a number')
                } else {
                    console.log(`Result: ${amount} ${from} equals ${(amount / currencies[from] * currencies[to]).toFixed(4)} ${to}`)
                }
            } else {
                console.log('Unknown currency')
            }
        } else {
            console.log('Unknown currency')
        }
    } else if (option === '2') {
        console.log('Have a nice day!')
        break
    }
    else {
        console.log('Unknown input')
    }
}