import random
import string


def check_letter(letter):
    global task, alphabet
    if letter not in alphabet:
        print('You\'ve already guessed this letter')
        return True
    alphabet = alphabet.replace(letter, '')
    flag = False
    for i in range(len(selected_word)):
        if selected_word[i] == letter:
            task = task[:i] + letter + task[i + 1:]
            flag = True
    return flag


def is_win():
    return '-' not in task


def already_in_word(letter):
    return letter in task


def is_valid_letter(letter):
    if len(letter) > 1:
        print('You should input a single letter\n')
        return False
    elif letter not in string.ascii_lowercase:
        print('Please enter a lowercase English letter\n')
        return False
    return True


def game_loop():
    global selected_word, task, alphabet
    alphabet = string.ascii_lowercase
    selected_word = random.choice(words)
    task = '-' * len(selected_word)
    print('H A N G M A N', end='\n\n')
    try_ = 0
    while True:
        print(task)
        letter_ = input('Input a letter:')
        if not is_valid_letter(letter_):
            continue
        if not check_letter(letter_):
            print('That letter doesn\'t appear in the word')
            try_ += 1
        if is_win():
            print('You guessed the word!\nYou survived!\n')
            break
        if try_ == 8:
            print('You lost!\n')
            break
        print()


if __name__ == '__main__':
    words = ['python', 'java', 'kotlin', 'javascript']
    alphabet = string.ascii_lowercase
    selected_word = ''
    task = ''
    while True:
        command = input('Type "play" to play the game, "exit" to quit: ')
        match command:
            case 'play':
                game_loop()
                break
            case 'exit':
                break
