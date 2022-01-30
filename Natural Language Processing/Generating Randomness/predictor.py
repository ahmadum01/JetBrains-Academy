from random import choice, sample

sequence = ''
MIN_LENGTH = 100


def append_data(data: str):
    global sequence
    for i in data:
        if i in '01':
            sequence += i


def count_triads():
    result = {}
    for i in range(len(sequence) - 3):
        temp = result.get(sequence[i: i + 3], [0, 0])
        temp[int(sequence[i + 3])] += 1
        result[sequence[i: i + 3]] = temp
    return result


def predict(test_string, triads):
    result = ''.join(sample('0011', 3))
    for i in range(0, len(test_string) - 3):
        temp = triads[test_string[i: i + 3]]
        if temp[0] == temp[1]:
            result += choice('01')
        else:
            result += str(temp.index(max(temp)))
    return result


def read_data():
    print('Please give AI some data to learn...')
    print('The current data length is 0, 100 symbols left')
    while len(sequence) < MIN_LENGTH:
        print('Print a random string containing 0 or 1:\n')
        append_data(input())
        if len(sequence) < MIN_LENGTH:
            print(f'Current data length is {len(sequence)}, {MIN_LENGTH - len(sequence)} symbols left')
    print('Final data string:', sequence, sep='\n', end='\n\n')


def right_digits_count(str1, str2):
    count = 0
    for i, j in zip(str1[3:], str2[3:]):
        if i == j:
            count += 1
    return count


def put_only_zero_and_one(string):
    result = ''
    for i in string:
        if i in '01':
            result += i
    return result


def main():
    read_data()
    triads = count_triads()
    balance = 1000
    print('You have $1000. Every time the system successfully predicts your next press, you lose $1.')
    print('Otherwise, you earn $1. Print "enough" to leave the game. Let\'s go!\n')
    while True:
        test_string = input('Print a random string containing 0 or 1:\n')
        if test_string == 'enough':
            print('Game over!')
            break
        test_string = put_only_zero_and_one(test_string)
        predict_string = predict(test_string, triads)
        right_digits = right_digits_count(test_string, predict_string)
        percent = right_digits / len(predict_string[3:]) * 100 if len(predict_string[3:]) else 0
        print('prediction:', predict_string, sep='\n')
        print(f'Computer guessed right {right_digits} out of {len(test_string) - 3} symbols ({percent} %)')
        balance -= right_digits * 2 - len(predict_string[3:])
        print(f'Your balance is now ${balance}', end='\n\n')


if __name__ == '__main__':
    main()
