import random
import re

while True:
    print('Which level do you want? Enter a number:')
    print('1 - simple operations with numbers 2-9')
    print('2 - integral squares of 11-29')
    level = input()
    if level in ['1', '2']:
        break
    print('Incorrect format.')

grade = 0
if level == '1':
    for i in range(5):
        expression = f'{random.randint(2, 9)} {random.choice("*-+")} {random.randint(2, 9)}'
        print(expression)
        while True:
            answer = input()
            if re.match(r'-?[\d]+$', answer):
                break
            print('Incorrect format.')
        if eval(expression) == int(answer):
            print('Right!')
            grade += 1
        else:
            print('Wrong!')
elif level == '2':
    for i in range(5):
        expression = random.randint(11, 29)
        print(expression)
        while True:
            answer = input()
            if re.match(r'-?[\d]+$', answer):
                break
            print('Incorrect format.')
        if expression ** 2 == int(answer):
            print('Right!')
            grade += 1
        else:
            print('Wrong!')

# Show and save result
if input(f'Your mark is {grade}/5. Would you like to save the result? Enter yes or no.\n').lower() in ['yes', 'y']:
    name = input('What is your name?')
    with open('results.txt', 'a') as file:
        if level == '1':
            file.write(f'{name}: {grade}/5 in level 1 (simple operations with numbers 2-9).\n')
        elif level == '2':
            file.write(f'{name}: {grade}/5 in level 1 (integral squares of 11-29).\n')
    print('The results are saved in "results.txt".')
