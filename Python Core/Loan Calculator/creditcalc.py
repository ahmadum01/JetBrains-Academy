import argparse
from math import ceil, log


def number_of_monthly_payments():
    p = int(args.principal)
    a = float(args.payment)
    i = float(args.interest) / 1200
    months_num = ceil(log(a/(a - i * p), 1 + i))
    years = months_num // 12
    months = months_num % 12
    if months and years:
        print(f'It will take {years} years and {months} months to repay this loan!')
    elif months:
        print(f'It will take {months} months to repay this loan!')
    else:
        print(f'It will take {years} years to repay this loan!')
    print('Overpayment =', (years * 12 + months) * a - p)


def annuity_monthly_payment():
    p = int(args.principal)
    n = int(args.periods)
    i = float(args.interest) / 1200
    a = ceil(p * i * (1 + i) ** n / ((1 + i) ** n - 1))
    print(f'Your monthly payment = {a}!')
    print('Overpayment =', n * a - p)


def loan_principal():
    a = float(args.payment)
    n = int(args.periods)
    i = float(args.interest) / 1200
    p = a / (i * (1 + i) ** n / ((1 + i) ** n - 1))
    print(f'Your loan principal = {p}!')
    print('Overpayment =', n * a - p)


def diff_monthly_payment():
    p = int(args.principal)
    n = int(args.periods)
    i = float(args.interest) / 1200
    summa = 0
    for k in range(1, n + 1):
        d = ceil(p / n + i * (p - (p * (k - 1) / n)))
        summa += d
        print('Month 3: payment is', d)
    print('Overpayment =', summa - p)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', nargs="?", default='')
    parser.add_argument('--principal', nargs="?", default='')
    parser.add_argument('--periods', nargs="?", default='')
    parser.add_argument('--interest', nargs="?", default='')
    parser.add_argument('--payment', nargs='?', default='')
    args = parser.parse_args()
    args_state = [args.type, args.principal, args.periods, args.interest, args.payment]

    if args_state.count('') != 1 or args.type not in ['annuity', 'diff'] or (args.type == 'diff' and args.payment) \
            or not args.interest or '-' in args.principal or '-' in args.periods or '-' in args.interest \
            or '-' in args.payment:
        print('Incorrect parameters')
    else:
        if args.type == 'annuity':
            if args.payment and args.periods and args.interest:
                loan_principal()
            elif args.principal and args.periods and args.interest:
                annuity_monthly_payment()
            else:
                number_of_monthly_payments()
        else:
            diff_monthly_payment()
