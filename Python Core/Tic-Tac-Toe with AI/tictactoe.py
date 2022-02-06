from random import choice


def print_game_field():
    print('---------')
    for line in game_field:
        print('|', *line, '|')
    print('---------')


def parse_coord(coordinates: list[str]) -> tuple[int, int]:
    return int(coordinates[0]) - 1, int(coordinates[1]) - 1


def get_turn(reverse: bool = False) -> 'O or X':
    x_count, o_count = 0, 0
    for line in game_field:
        x_count += line.count('X')
        o_count += line.count('O')
    if reverse:
        return 'X' if o_count < x_count else 'O'
    return 'X' if o_count >= x_count else 'O'


def set_move(coordinates: tuple[int, int]):
    turn = get_turn()
    game_field[coordinates[0]][coordinates[1]] = turn


def is_win(board, player) -> bool:
    """Winning combinations using the board indexes"""
    if (board[0][0] == player and board[0][1] == player and board[0][2] == player) or \
            (board[1][0] == player and board[1][1] == player and board[1][2] == player) or \
            (board[2][0] == player and board[2][1] == player and board[2][2] == player) or \
            (board[0][0] == player and board[1][0] == player and board[2][0] == player) or \
            (board[0][1] == player and board[1][1] == player and board[2][1] == player) or \
            (board[0][2] == player and board[1][2] == player and board[2][2] == player) or \
            (board[0][0] == player and board[1][1] == player and board[2][2] == player) or \
            (board[2][0] == player and board[1][1] == player and board[0][2] == player):
        return True
    else:
        return False


def get_empty_cells() -> list[tuple[int, int]]:
    """Return coordinates of empty board's cells"""
    result = []
    for i in range(len(game_field)):
        for j in range(len(game_field)):
            if game_field[i][j] == ' ':
                result.append((i, j))
    return result


def computer_easy_move():
    """Easy AI level"""
    coordinates = choice(get_empty_cells())
    set_move(coordinates)


def computer_medium_move():
    """Medium AI level"""
    turn = get_turn()
    patterns = {'X': [' XX', 'X X', 'XX '], 'O': [' OO', 'O O', 'OO ']}
    for turn in [get_turn(), get_turn(reverse=True)]:
        for line in range(len(game_field)):  # Horizontal
            temp = ''.join(game_field[line])
            if temp in patterns[turn]:
                set_move((line, temp.find(' ')))
                return
        for line in range(len(game_field)):  # Verticals
            temp = game_field[0][line] + game_field[1][line] + game_field[2][line]
            if temp in patterns[turn]:
                set_move((temp.find(' '), line))
                return
        # Diagonals
        temp = game_field[0][0] + game_field[1][1] + game_field[2][2]
        if temp in patterns[turn]:
            set_move((temp.find(' '), temp.find(' ')))
            return
        temp = game_field[0][2] + game_field[1][1] + game_field[2][0]
        if temp in patterns[turn]:
            n = temp.find(' ')
            match n:
                case 0:
                    set_move((0, 2))
                    return
                case 1:
                    set_move((1, 1))
                    return
                case 2:
                    set_move((2, 0))
                    return
    computer_easy_move()


def computer_hard_move():
    """Medium AI level and Wrapper for minimax function"""
    def minimax(new_board, player):
        """The main minimax function"""
        avail_cells = get_empty_cells()  # available cells
        # checks for the terminal states such as win, lose, and tie and returning a value accordingly
        if is_win(new_board, hu_player):
            return {'score': -10, 'index': (0, 0)}
        elif is_win(new_board, ai_player):
            return {'score': 10, 'index': (0, 0)}
        elif len(avail_cells) == 0:
            return {'score': 0, 'index': (0, 0)}
        # an array to collect all the objects
        moves = []
        # loop through available cells
        for i in range(len(avail_cells)):
            # Create an object for each and store the index of that cell
            # that was stored as a number in the object's index key
            move = {'score': 0, 'index': avail_cells[i]}

            # set the empty cell to the current player
            new_board[avail_cells[i][0]][avail_cells[i][1]] = player

            if player == ai_player:
                result = minimax(new_board, hu_player)
                move['score'] = result['score']
            else:
                result = minimax(new_board, ai_player)
                move['score'] = result['score']
            # reset the cell to empty
            new_board[avail_cells[i][0]][avail_cells[i][1]] = ' '
            moves.append(move)

        if player == ai_player:  # choose the move with the highest score
            best_move = moves.index(max(moves, key=lambda m: m['score']))
        else:  # choose the move with the lowest score
            best_move = moves.index(min(moves, key=lambda m: m['score']))
        return moves[best_move]

    ai_player = get_turn()
    hu_player = get_turn(True)
    set_move(minimax(game_field, ai_player)['index'])


def take_user_input():
    while True:
        coord = input().split()
        if not len(coord) == 2 or not (coord[0].isdigit() or coord[1].isdigit()):
            print('You should enter numbers!')
        elif not (0 <= parse_coord(coord)[0] <= 2 and 0 <= parse_coord(coord)[1] <= 2):
            print('Coordinates should be from 1 to 3!')
        elif game_field[parse_coord(coord)[0]][parse_coord(coord)[1]] != ' ':
            print('This cell is occupied! Choose another one!')
        else:
            return coord


def game_loop(player1, player2):
    players = [player1, player2]
    reset_field()
    print_game_field()
    switcher = 0

    while True:
        match players[switcher % 2]:
            case 'user':
                print('Enter the coordinates: ', end='')
                set_move(parse_coord(take_user_input()))
            case 'easy':
                print('Making move level "easy"')
                computer_easy_move()
            case 'medium':
                print('Making move level "medium"')
                computer_medium_move()
            case 'hard':
                print('Making move level "hard"')
                computer_hard_move()
        print_game_field()
        if is_win(game_field, get_turn(reverse=True)):
            print(f'{get_turn(reverse=True)} wins')
            break
        if len(get_empty_cells()) == 0:
            print('Draw')
            break
        switcher += 1


def reset_field():
    global game_field
    game_field = [[' ', ' ', ' '],
                  [' ', ' ', ' '],
                  [' ', ' ', ' ']]


if __name__ == '__main__':
    game_field = ...

    mods = ['user', 'easy', 'medium', 'hard']
    while True:
        command = input('Input command: ').split()
        if len(command) == 3 and command[0] == 'start' and command[1] in mods and command[2] in mods:
            game_loop(command[1], command[2])
        elif command == ['exit']:
            break
        else:
            print('Bad parameters!')
