from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker


ENGINE = create_engine('sqlite:///flashcard.db?check_same_thread=False')
Base = declarative_base()


class FlashCardModel(Base):
    __tablename__ = 'flashcard'
    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    box = Column(Integer, default=1)


class FlashCards:
    def __init__(self):
        self.flashcards = []
        Base.metadata.create_all(ENGINE)
        self.session = sessionmaker(bind=ENGINE)()

    def add(self):
        while True:
            question = input('\nQuestion:\n')
            if not question.isspace() and question:
                break
        while True:
            answer = input('Answer:\n')
            if not answer.isspace() and answer:
                break
        self.session.add(FlashCardModel(question=question, answer=answer))
        self.session.commit()

    def practice(self):
        data = self.session.query(FlashCardModel).all()
        if not data:
            print('There is no flashcard to practice!')
        else:
            for flash_card in data:
                self.show(flash_card)

    def show(self, flash_card: FlashCardModel):
        print('\nQuestion:', flash_card.question)
        match input('press "y" to see the answer:\npress "n" to skip:\npress "u" to update:\n'):
            case 'y':
                print(f'Answer: {flash_card.answer}')
                if input('\npress "y" if your answer is correct:\n'
                         'press "n" if your answer is wrong:\n') == 'y':
                    self.move_to_next_box(flash_card)
                else:
                    flash_card.box = 1
                    self.session.commit()
            case 'n': self.move_to_next_box(flash_card)
            case 'u': self.update_menu(flash_card)

    def move_to_next_box(self, flash_card: FlashCardModel):
        if flash_card.box == 3:
            self.session.delete(flash_card)
        else:
            flash_card.box += 1
        self.session.commit()

    def update_menu(self, flashcard: FlashCardModel):
        match input('press "d" to delete the flashcard:\npress "e" to edit the flashcard:\n'):
            case 'd':
                self.session.delete(flashcard)
                self.session.commit()
            case 'e': self.edit(flashcard)

    def edit(self, flashcard: FlashCardModel):
        new_question = input(f'\ncurrent question: {flashcard.question}\nplease write a new question:\n')
        new_answer = input(f'\ncurrent answer: {flashcard.answer}\nplease write a new answer:\n')
        if new_question:
            flashcard.question = new_question
        if new_answer:
            flashcard.answer = new_answer
        self.session.commit()

    def add_cards_menu(self):
        while True:
            match input('\n1. Add a new flashcard\n2. Exit\n'):
                case '1': self.add()
                case '2': break
                case _ as wrong_key: print(f'{wrong_key} is not an option')

    def main_loop(self):
        while True:
            match input('\n1. Add flashcards\n2. Practice flashcards\n3. Exit\n'):
                case '1': self.add_cards_menu()
                case '2': self.practice()
                case '3':
                    print('\nBye!')
                    break
                case _ as wrong_key: print(f'{wrong_key} is not an option')


if __name__ == '__main__':
    flash_cards = FlashCards()
    flash_cards.main_loop()
