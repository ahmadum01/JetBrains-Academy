FORMATS = ['plain', 'bold', 'italic', 'header', 'link', 'inline-code', 'new-line', 'ordered-list', 'unordered-list']
result = ''


def plain():
    global result
    result += input('Text: ')


def bold():
    global result
    result += f"**{input('Text: ')}**"


def italic():
    global result
    result += f"*{input('Text: ')}*"


def header():
    global result
    while True:
        level = int(input('Level: '))
        if 1 <= level <= 6:
            break
        print('The level should be within the range of 1 to 6')
    result += f"{'#' * level} {input('Text: ')}\n"


def link():
    global result
    result += f"[{input('Label: ')}]({input('URL: ')})"


def inline_code():
    global result
    result += f"`{input('Text: ')}`"


def new_line():
    global result
    result += '\n'


def ordered_list():
    global result
    while True:
        num_of_rows = int(input('Number of rows: '))
        if num_of_rows > 0:
            for i in range(num_of_rows):
                result += f"{i + 1}. {input(f'Row #{i + 1}: ')}\n"
            break
        else:
            print('The number of rows should be greater than zero')


def unordered_list():
    global result
    while True:
        num_of_rows = int(input('Number of rows: '))
        if num_of_rows > 0:
            for i in range(num_of_rows):
                result += f"* {input(f'Row #{i + 1}: ')}\n"
            break
        else:
            print('The number of rows should be greater than zero')


def get_function(function_name):
    match function_name:
        case 'plain': return plain
        case 'bold': return bold
        case 'italic': return italic
        case 'header': return header
        case 'link': return link
        case 'inline-code': return inline_code
        case 'new-line': return new_line
        case 'ordered-list': return ordered_list
        case 'unordered-list': return unordered_list


if __name__ == '__main__':
    while True:
        match input('Choose a formatter: '):
            case '!help':
                print(f'Available formatters: {" ".join(FORMATS)}')
                print('Special commands: !help !done')
            case '!done':
                with open('output.md', 'w') as file:
                    file.write(result)
                break
            case format_type if format_type in FORMATS:
                get_function(format_type)()
                print(result)
            case _:
                print('Unknown formatting type or command')
