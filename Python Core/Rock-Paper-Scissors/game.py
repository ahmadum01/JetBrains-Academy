import random

objects = ['paper', 'scissors', 'rock']


def result(user, computer):
    if user == computer:
        return 'Draw'
    index = objects.index(user)
    for i in range(1, len(objects) // 2 + 1):
        if computer == objects[index - i]:
            return 'Win'
    return 'Lose'


def game_loop():
    global objects
    with open('rating.txt', 'r') as file:
        rating = {line.split()[0]: int(line.split()[1]) for line in file.readlines()}
    name = input('Enter your name: ')
    print(f'Hello, {name}')
    score = rating.get(name, 0)
    new_objects = input().split(',')
    if len(new_objects) > 2:
        objects = new_objects
    print('Okay, let\'s start')
    while True:
        match input().lower():
            case user_input if user_input in objects:
                computer = random.choice(objects)
                match result(user_input, computer):
                    case 'Draw':
                        print(f'There is a draw ({computer})')
                        score += 50
                    case 'Lose':
                        print(f'Sorry, but the computer chose {computer}')
                    case 'Win':
                        print(f'Well done. The computer chose {computer} and failed')
                        score += 100
            case '!exit':
                print('Bye!')
                break
            case '!rating':
                print(f'Your rating: {score}')
            case _:
                print('Invalid input')


if __name__ == '__main__':
    game_loop()
