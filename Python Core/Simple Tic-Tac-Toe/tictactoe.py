class Tictactoe:
    def __init__(self):
        self.field = '_' * 9

    def print(self):
        print('-' * 9)
        for i in range(0, 9, 3):
            print('|', ' '.join(self.field[i: i + 3]), '|')
        print('-' * 9)

    def game_state(self):
        def state(sym):
            temp = [self.field[0] + self.field[1] + self.field[2] == sym,
                    self.field[3] + self.field[4] + self.field[5] == sym,
                    self.field[6] + self.field[7] + self.field[8] == sym,
                    self.field[0] + self.field[3] + self.field[6] == sym,
                    self.field[1] + self.field[4] + self.field[7] == sym,
                    self.field[2] + self.field[5] + self.field[8] == sym,
                    self.field[0] + self.field[4] + self.field[8] == sym,
                    self.field[2] + self.field[4] + self.field[6] == sym]
            return any(temp)

        state_o, state_x = state('OOO'), state('XXX')
        count_o, count_x = self.field.count('O'), self.field.count('X')
        if state_o and state_x or abs(count_x - count_o) > 1:
            return 'Impossible'
        if state_o:
            return 'O wins'
        if state_x:
            return 'X wins'
        if '_' not in self.field:
            return 'Draw'
        return 'Game not finished'

    def get_coord(self):
        while True:
            coord = input('Enter the coordinates:').split()
            if len(coord) != 2 or not coord[0].isdigit() or not coord[1].isdigit():
                print('You should enter numbers!')
            elif not 1 <= int(coord[0]) <= 3 or not 1 <= int(coord[1]) <= 3:
                print('Coordinates should be from 1 to 3!')
            elif self.field[(int(coord[0]) - 1) * 3 + (int(coord[1]) - 1)] != '_':
                print('This cell is occupied! Choose another one!')
            else:
                return coord

    def move(self, coord, sym):
        index = (int(coord[0]) - 1) * 3 + (int(coord[1]) - 1)
        self.field = self.field[:index] + sym + self.field[index + 1:]

    def start(self):
        players = ['X', 'O']
        turn = 0
        self.print()
        while True:
            self.move(self.get_coord(), players[turn % 2])
            command = self.game_state()
            self.print()
            if 'wins' in command or 'Draw' in command:
                print(command)
                break
            turn += 1


if __name__ == '__main__':
    game = Tictactoe()
    game.start()
