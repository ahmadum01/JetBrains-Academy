import requests
import json


def get_currency_info(base, currency=None, first=False):
    """Get currency info from floatrates.com and save it to the cash"""
    url = f"http://www.floatrates.com/daily/{base.lower()}.json"
    req = requests.get(url)
    if first:
        match base:
            case 'usd': save_to_cash(json.loads(req.content), 'eur')
            case 'eur': save_to_cash(json.loads(req.content), 'usd')
            case _:     save_to_cash(json.loads(req.content), 'usd', 'eur')
    else:
        save_to_cash(json.loads(req.content), currency)


def save_to_cash(data, *currency):
    for i in currency:
        cash[i] = data[i]['inverseRate']


if __name__ == '__main__':
    cash = {}
    base_currency = input().lower()
    get_currency_info(base_currency, first=True)
    while True:
        currency_ = input().lower()
        if not currency_:
            break
        amount = int(input())
        print('Checking the cache...')
        if currency_ in cash:
            print('Oh! It is in the cache!')
            print(f'You received {amount / cash[currency_]} {currency_.upper()}.')
        else:
            print('Sorry, but it is not in the cache!')
            get_currency_info(base_currency, currency_)
            print(f'You received {amount / cash[currency_]} {currency_.upper()}.')

