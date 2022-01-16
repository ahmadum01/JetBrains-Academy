class Board:
    def __init__(self, w: int, h: int):
        self.w = w
        self.h = h
        self.cell_size = len(str(h * w))
        self.h_length = len(str(h))
        self.board = [['_' * self.cell_size for i in range(w)] for _ in range(h)]
        self.current_pos = None

    def copy(self):
        """Returns copy of Board object"""
        new_board = Board(self.w, self.h)
        new_board.board = [[cell for cell in line] for line in self.board]
        new_board.current_pos = self.current_pos
        return new_board

    def print(self):
        """Prints a board"""
        print(" " * self.h_length + "-" * ((self.cell_size + 1) * self.w + 3))
        for i in range(self.h):
            print(f"{' ' * (self.h_length - len(str(self.h - i)))}{self.h - i}| {' '.join(self.board[i])} |")
        print(" " * self.h_length + "-" * ((self.cell_size + 1) * self.w + 3))
        print(f'{" " * (self.h_length + 2)}'
              f'{" ".join([" " * (self.cell_size - 1) + str(i) for i in range(1, self.w + 1)])}\n')

    def set_pos(self, coord: tuple[int, int], sym):
        """set position"""
        self.board[coord[1]][coord[0]] = ' ' * (self.cell_size - 1) + sym

    def is_possible_move(self, x1, y1, x2, y2) -> bool:
        return (abs(x1 - x2), abs(y1 - y2)) in [(1, 2), (2, 1)] and 0 <= x2 <= self.w - 1\
            and 0 <= y2 <= self.h - 1 and '*' not in self.board[y2][x2]

    def possible_moves(self, coord: tuple[int, int]):
        result = []
        for y in range(self.h):
            for x in range(self.w):
                if self.is_possible_move(*coord, x, y):
                    result.append((x, y))
        return result

    def num_possible_moves(self, coord: tuple[int, int]):
        self.set_pos(coord, 'X')
        poss_moves = self.possible_moves(coord)
        for i in poss_moves:
            self.set_pos(i, str(len(self.possible_moves(i)) - 1))

    def move(self, coord: tuple[int, int]):
        for i in range(self.h):
            for j in range(self.w):
                if self.board[i][j] == ' ' * (self.cell_size - 1) + 'X':
                    self.board[i][j] = ' ' * (self.cell_size - 1) + '*'
                elif self.board[i][j] != ' ' * (self.cell_size - 1) + '*':
                    self.board[i][j] = '_' * self.cell_size
        self.current_pos = coord
        self.num_possible_moves(coord)

    def board_state(self):
        empty_cell_flag = False
        stars_count = 0
        for i in range(self.h):
            for j in range(self.w):
                match self.board[i][j]:
                    case cell if cell.strip().isdigit():
                        return 'Continue'
                    case cell if '_' in cell:
                        empty_cell_flag = True
                    case cell if '*' in cell:
                        stars_count += 1
        if empty_cell_flag:
            return 'Lose', stars_count + 1
        return 'Win'

    def set_starting_position(self):
        while True:
            match input('Enter the knight\'s starting position: ').split():
                case x, y, if x.isdigit() and y.isdigit() and 1 <= int(x) <= self.w and 1 <= int(y) <= self.h:
                    coordinates = int(x) - 1, self.h - int(y)
                    self.current_pos = coordinates
                    self.move(coordinates)
                    return coordinates
                case _:
                    print('Invalid dimensions!')

    def fill(self, solve: list[tuple]):
        """Fill board with solve"""
        solve.insert(0, self.current_pos)
        for i in range(len(solve)):
            x, y = solve[i]
            self.board[y][x] = ' ' * (self.cell_size - len(str(i + 1))) + str(i + 1)


def get_coord(board: Board):
    label = 'Enter your next move: '
    while True:
        match input(label).split():
            case x, y, if x.isdigit() and y.isdigit() \
                          and board.is_possible_move(*board.current_pos, int(x) - 1, board.h - int(y)):
                return int(x) - 1, board.h - int(y)
            case _:
                if 'Invalid move!' not in label:
                    label = 'Invalid move! ' + label


def get_board_size() -> tuple:
    while True:
        match input('Enter your board dimensions: ').split():
            case w, h, if w.isdigit() and h.isdigit() and 1 <= int(w) and 1 <= int(h):
                return int(w), int(h)
            case _:
                print('Invalid dimensions!')


def solver(board: Board, possible_positions: list[tuple[int, int]]):
    result = []
    for position in possible_positions:
        new_board = board.copy()
        new_board.move(position)
        match new_board.board_state():
            case 'Continue':
                temp = solver(new_board, new_board.possible_moves(new_board.current_pos))
                if isinstance(temp, list):
                    result += [position] + temp
                    return result
                continue
            case 'Win':
                result.append(position)
                return result
            case 'Lose', steps:
                return False


def game_loop(board: Board):
    board.print()
    while True:
        coord = get_coord(board)
        if coord:
            board.move(coord)
            board.print()
        match board.board_state():
            case 'Continue':
                continue
            case 'Lose', steps:
                print('No more possible moves!')
                print(f'Your knight visited {steps} squares!')
                break
            case 'Win':
                print('What a great tour! Congratulations!')
                break


if __name__ == '__main__':
    chess_board = Board(*get_board_size())
    chess_board.set_starting_position()
    temp_ = solver(chess_board, chess_board.possible_moves(chess_board.current_pos))
    while True:
        match input('Do you want to try the puzzle? (y/n): '):
            case 'y':
                if not temp_:
                    print('No solution exists!')
                else:
                    game_loop(chess_board)
                break
            case 'n':
                if not temp_:
                    print('No solution exists!')
                else:
                    print('\nHere\'s the solution!')
                    board_with_solve = chess_board.copy()
                    board_with_solve.fill(temp_)
                    board_with_solve.print()
                break
            case _:
                print('Invalid input!')
