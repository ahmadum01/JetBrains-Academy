import re

msgs = ["Enter an equation",
        "Do you even know what numbers are? Stay focused!",
        "Yes ... an interesting math operation. You've slept through all classes, haven't you?",
        "Yeah... division by zero. Smart move...",
        "Do you want to store the result? (y / n):",
        "Do you want to continue calculations? (y / n):",
        " ... lazy",
        " ... very lazy",
        " ... very, very lazy",
        "You are",
        "Are you sure? It is only one digit! (y / n)",
        "Don't be silly! It's just one number! Add to the memory? (y / n)",
        "Last chance! Do you really want to embarrass yourself? (y / n)"]


def is_one_digit(num: str):
    return bool(re.match(r'\d(\.0)?$', num))


def check(v1, v2, v3):
    msg = ''
    if is_one_digit(v1) and is_one_digit(v2):
        msg += msgs[6]
    if (v1 == '1' or v2 == '1') and v3 == '*':
        msg += msgs[7]
    if (v1 == '0' or v2 == '0') and (v3 in '*+-'):
        msg += msgs[8]
    if msg != '':
        print(msgs[9] + msg)


def main_loop():
    M = 0
    while True:
        x, operator, y = input(msgs[0]).split()
        if x == 'M':
            x = str(M)
        if y == 'M':
            y = str(M)
        if not re.match(r'-?(\d+|\d+\.\d+)$', x) or not re.match(r'-?(\d+|\d+\.\d+)$', y):
            print(msgs[1])
        elif y == '0' and operator == '/':
            check(x, y, operator)
            print(msgs[3])
        else:
            match operator:
                case '+':
                    result = float(x) + float(y)
                case '-':
                    result = float(x) - float(y)
                case '*':
                    result = float(x) * float(y)
                case '/':
                    result = float(x) / float(y)
                case _:
                    print(msgs[2]); continue
            check(x, y, operator)
            print(result)
            if input(msgs[4]) == 'y':
                if is_one_digit(str(result)):
                    msg_index = 10
                    while True:
                        command = input(msgs[msg_index])
                        if command == 'y':
                            if msg_index == 12:
                                M = result
                                break
                            msg_index += 1
                        elif command == 'n':
                            break
                else:
                    M = result
            if input(msgs[5]) != 'y':
                break


if __name__ == '__main__':
    main_loop()
