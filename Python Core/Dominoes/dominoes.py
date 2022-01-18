import random
import re


class DominoGame:
    def __init__(self):
        self.stock = [...]
        self.player = [...]
        self.computer = [...]
        self.order = [..., ...]
        self.snake = []

    def delete_elements(self, dominoes):
        """Delete elements from stock """
        for domino in dominoes:
            self.stock.remove(domino)

    def find_highest_double(self):
        """Double examples: [0, 0], [1, 1], [6, 6]"""
        max_domino_player = [-1, -1]
        max_domino_computer = [-1, -1]
        for i in range(7):
            if self.player[i][0] == self.player[i][1] and self.player[i] > max_domino_player:
                max_domino_player = self.player[i]
            if self.computer[i][0] == self.computer[i][1] and self.computer[i] > max_domino_computer:
                max_domino_computer = self.computer[i]
        if max_domino_player == max_domino_computer:
            return 'There is no Double'
        if max_domino_player > max_domino_computer:
            self.order = ['player', 'computer']
            self.player.remove(max_domino_player)
            return max_domino_player
        else:
            self.order = ['computer', 'player']
            self.computer.remove(max_domino_computer)
            return max_domino_computer

    def generate_start_state(self):
        while True:
            self.stock = [[i, j] for i in range(7) for j in range(i, 7)]
            self.player = random.sample(self.stock, 7)
            self.delete_elements(self.player)
            self.computer = random.sample(self.stock, 7)
            self.delete_elements(self.computer)
            match self.find_highest_double():
                case 'There is no Double':
                    self.generate_start_state()
                case domino:
                    self.snake.append(domino)
                    break

    def print(self):
        print('=' * 70)
        print('Stock size:', len(self.stock))
        print('Computer pieces:', len(self.computer), end='\n\n')
        if len(self.snake) > 6:
            print(*self.snake[:3], '...', *self.snake[-3:], sep='', end='\n\n')
        else:
            print(*self.snake, end='\n\n')
        print('Your pieces:')
        for num, domino in enumerate(self.player, 1):
            print(f'{num}:{domino}')

    def computer_statistic(self) -> list:
        statistic = {}
        for domino in self.computer + self.snake:
            for num in domino:
                statistic[num] = statistic.get(num, 0) + 1
        return sorted(self.computer, key=lambda domino_: statistic[domino_[0]] + statistic[domino_[1]], reverse=True)

    def computer_move(self):
        input('\nStatus: Computer is about to make a move. Press Enter to continue...\n')
        for domino in self.computer_statistic():
            if self.snake[0][0] in domino:
                self.snake.insert(0, self.reorient(domino, 'left'))
                self.computer.remove(domino)
                break
            if self.snake[-1][-1] in domino:
                self.snake.append(self.reorient(domino, 'right'))
                self.computer.remove(domino)
                break
        else:
            if self.stock:
                domino = random.choice(self.stock)
                self.computer.append(domino)
                self.stock.remove(domino)

    def player_move(self):
        number = input('\nStatus: It\'s your turn to make a move. Enter your command.\n')
        while True:
            if re.match(r'-?\d$', number) and -len(self.player) <= int(number) <= len(self.player):
                match int(number):
                    case 0:
                        if self.stock:
                            domino = random.choice(self.stock)
                            self.player.append(domino)
                            self.stock.remove(domino)
                        break
                    case num if num > 0:
                        domino = self.player[num - 1]
                        if self.snake[-1][-1] in domino:
                            self.snake.append(self.reorient(domino))
                            self.player.remove(domino)
                            break
                        print('Illegal move. Please try again.')
                    case num if num < 0:
                        domino = self.player[abs(num) - 1]
                        if self.snake[0][0] in domino:
                            self.snake.insert(0, self.reorient(domino, 'left'))
                            self.player.remove(domino)
                            break
                        print('Illegal move. Please try again.')
            else:
                print('Invalid input. Please try again.')
            number = input()

    def game_status(self):
        if len(self.computer) == 0:
            return 'Status: The game is over. The computer won!'
        if len(self.player) == 0:
            return 'Status: The game is over. You won!'
        first_num, second_num = self.snake[0][0], self.snake[-1][-1]
        count = 0
        for domino in self.snake:
            for num in domino:
                if num == first_num:
                    count += 1
        if first_num == second_num and count == 8:
            return 'Status: The game is over. It\'s a draw!'

    def reorient(self, domino, side='right'):
        temp = domino[:]
        match side:
            case 'right':
                if self.snake[-1][1] == domino[0]:
                    return domino
                temp[0], temp[1] = temp[1], temp[0]
                return temp
            case 'left':
                if self.snake[0][0] == domino[1]:
                    return domino
                temp[0], temp[1] = temp[1], temp[0]
                return temp

    def start(self):
        self.generate_start_state()
        turn = 1
        while True:
            self.print()
            match self.order[turn % 2]:
                case 'player': self.player_move()
                case 'computer': self.computer_move()
            command = self.game_status()
            match command:
                case 'Status: The game is over. The computer won!':
                    self.print()
                    print(command)
                    break
                case 'Status: The game is over. You won!':
                    self.print()
                    print(command)
                    break
                case 'Status: The game is over. It\'s a draw!':
                    self.print()
                    print(command)
                    break
            turn += 1


if __name__ == '__main__':
    game = DominoGame()
    game.start()
