import random

n = int(input('Enter the number of friends joining (including you):\n'))
if n > 0:
    print('\nEnter the name of every friend (including you), each on a new line:')
    people = []
    for i in range(n):
        people.append(input())
    amount = int(input('\nEnter the total bill value:\n'))

    match input('\nDo you want to use the "Who is lucky?" feature? Write Yes/No:\n'):
        case 'Yes':
            lucky_man = random.choice(people)
            print(f'\n{lucky_man} is the lucky one!\n')
            people = dict.fromkeys(people, round(amount / (len(people) - 1)))
            people[lucky_man] = 0
            print(people)
        case 'No':
            print('No one is going to be lucky\n')
            print(dict.fromkeys(people, round(amount / len(people), 2)))
else:
    print('No one is joining for the party')