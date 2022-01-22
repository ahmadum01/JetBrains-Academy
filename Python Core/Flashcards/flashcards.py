import argparse
import os
from io import StringIO


class Card:
    def __init__(self, term, definition, mistakes=0):
        self.front = term
        self.back = definition
        self.mistakes = mistakes

    def __eq__(self, obj):
        if self.front == obj.front:
            return True
        return False


class Cards:
    def __init__(self):
        self.cards = []
        self.cards_front = {}
        self.cards_back = {}
        self.cards_mistake = {}
        self.log_lines = []
        self.buffer = StringIO()

    def add_card(self, card):
        self.cards.append(card)
        self.cards_front[card.front] = card.back
        self.cards_back[card.back] = card.front
        self.cards_mistake[card.front] = card.mistakes

    def replace_card(self, card, index):
        self.cards[index] = card
        self.cards_front[card.front] = card.back
        self.cards_back[card.back] = card.front
        self.cards_mistake[card.front] = card.mistakes

    def create_new_card(self):
        term = self.input_and_log(f'The card:\n')
        while self.cards_front.get(term, False):
            term = self.input_and_log(f'The term "{term}" already exists. Try again:\n')
        definition = self.input_and_log(f'The definition of the card::\n')
        while self.cards_back.get(definition, False):
            definition = self.input_and_log(f'The definition "{definition}" already exists. Try again:\n')
        self.add_card(Card(term, definition))
        self.print_and_log(f'The pair ("{term}":"{definition}") has been added.\n')

    def remove_card(self):
        term = self.input_and_log('Which card?\n')
        for card in self.cards:
            if term == card.front:
                self.cards_front.pop(card.front)
                self.cards_back.pop(card.back)
                self.cards_mistake.pop(card.front)
                self.cards.remove(card)
                self.print_and_log('The card has been removed.\n')
                return
        self.print_and_log(f'Can\'t remove "{term}": there is no such card.\n')

    def import_cards(self, file_name=None):
        if not file_name:
            file_name = self.input_and_log('File name:\n')
        print(file_name+'*')
        if file_name in os.listdir():
            with open(file_name, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    loaded_card = line.split(':')
                    loaded_card = Card(loaded_card[0], loaded_card[1], int(loaded_card[2].strip()))
                    for index, card in enumerate(self.cards):
                        if card == loaded_card:
                            self.replace_card(loaded_card, index)
                            break
                    else:
                        self.add_card(loaded_card)
                self.print_and_log(f'{len(lines)} cards have been loaded.\n')
        else:
            self.print_and_log('File not found.\n')

    def export_cards(self, file_name=None):
        if not file_name:
            file_name = self.input_and_log('File name:\n')
        with open(file_name, 'w') as file:
            for card in self.cards:
                file.write(':'.join([card.front, card.back, str(card.mistakes)]) + '\n')
        self.print_and_log(f'{len(self.cards)} cards have been saved.\n')

    def ask(self):
        """Ask N terms from cards"""
        numbers = int(self.input_and_log('How many times to ask?\n'))
        for i in range(numbers):
            answer = self.input_and_log(f'Print the definition of "{self.cards[i % len(self.cards)].front}":\n')
            if self.cards[i % len(self.cards)].back == answer:
                self.print_and_log('Correct!\n')
            elif self.cards_back.get(answer, False):
                self.print_and_log(f'Wrong. The right answer is "ankle", but your definition \
is correct for "{self.cards_back[answer]}".\n')
                self.cards[i % len(self.cards)].mistakes += 1
            else:
                self.print_and_log(f'Wrong. The right answer is "{self.cards[i % len(self.cards)].back}".\n')
                self.cards[i % len(self.cards)].mistakes += 1

    def print_and_log(self, text):
        """Simple print with saving outputs into buffer"""
        self.buffer.write(text+'\n')
        print(text)

    def input_and_log(self, text):
        """Simple input with saving outputs into buffer"""
        inp = input(text)
        self.buffer.write(text)
        self.buffer.write(inp + '\n')
        return inp

    def log(self):
        """Saves all inputs and outputs in file 'file_name' """
        file_name = self.input_and_log('File name:\n')
        with open(file_name, 'w') as file:
            print(self.buffer.getvalue(), file=file, flush=True)
        self.print_and_log('The log has been saved.\n')

    def hardest_card(self):
        """Show card/cards with max quantity of mistakes"""
        hardest_card_list = []
        max_mistakes = 0
        for card in self.cards:
            if card.mistakes > max_mistakes:
                hardest_card_list = [card.front]
                max_mistakes = card.mistakes
            elif card.mistakes == max_mistakes:
                hardest_card_list.append(card.front)
        if max_mistakes == 0:
            self.print_and_log('There are no cards with errors.\n')
        elif len(hardest_card_list) == 1:
            self.print_and_log(f'The hardest card is "{hardest_card_list[0]}". You have {max_mistakes} errors answering it.\n')
        else:
            out_str = ','.join([f'"{i}"' for i in hardest_card_list])
            self.print_and_log(f'The hardest cards are {out_str}. You have {max_mistakes} errors answering them.\n')

    def reset_stats(self):
        """Reset values of mistakes to zero"""
        for card in self.cards:
            card.mistakes = 0
        self.print_and_log('Card statistics have been reset.\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--import_from")  # Initialisation 'import_from' command line argument
    parser.add_argument("--export_to")  # Initialisation 'export_to' command line argument
    args = parser.parse_args()
    cards = Cards()
    if args.import_from:
        cards.import_cards(args.import_from)
    while True:  # Main loop
        command = cards.input_and_log('Input the action (add, remove, import, export, ask, exit, \
log, hardest card, reset stats):\n')
        match command:
            case 'add': cards.create_new_card()
            case 'remove': cards.remove_card()
            case 'import': cards.import_cards()
            case 'export': cards.export_cards()
            case 'ask': cards.ask()
            case 'log': cards.log()
            case 'hardest card': cards.hardest_card()
            case 'reset stats': cards.reset_stats()
            case 'exit':
                if args.export_to:
                    cards.export_cards(args.export_to)
                cards.print_and_log('Bye bye!')
                break


if __name__ == '__main__':
    main()
