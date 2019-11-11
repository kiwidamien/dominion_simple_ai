'''
Former code:
       menu="""
Modify hand before playing:
"1 N" Discard to N cards
"2 N" Draw N cards
"3"   Add curse to discard
"4"   Add curse to hand
"5"   Add curse to deck
Or press enter to continue
"""
        choice = 'first'
        while choice[0] not in ['1', '2', '3', '4', '5']:
            if choice != 'first':
                print("Invalid choice")
            choice = input(menu)
            if (len(choice) == 0) or choice == '\n':
                return
        if choice[0] == '3':
            self.add_curse('discard')
        if choice[0] == '4':
            self.add_curse('hand')
        if choice[0] == '5':
            self.add_curse('deck')
        if choice[0] == '2':
            print(choice.split()[-1])
            n_cards = int(choice.split()[-1])
            self.draw_n_cards(n_cards)
        if choice[0] == '1':
            n_cards = int(choice.split()[-1])
            self.discard_n_cards(n_cards)
        # might be multiple preprocessing steps
        self.preprocess_hand()
​
    def do_turn(self):
        if self.need_preprocessing:
            self.modification_stage = True
            self.preprocess_hand()
            self.modification_stage = False
        self.report()
        self.play_hand()
        self.draw_hand()
​
'''

from abc import ABC, abstractmethod
from typing import List


from dominion_ai.abstract_player import Player

class MenuItem(ABC):
    def __init__(self, prompt: str, player: Player):
        self.prompt = prompt
        self.player = player

    @abstractmethod
    def validate(self, choice: List[str]) -> bool:
        pass

    def __str__(self):
        return self.prompt

    @abstractmethod
    def action(self, choice: List[str]):
        if not self.validate(choice):
            raise ValueError(f'Invalid choice for menu item: {choice}')


class PlayGameItem(MenuItem):
    def __init__(self, player: Player):
        super().__init__('Have bot play hand', player)

    def validate(self, choice: List[str]) -> bool:
        return len(choice) == 0

    def action(self, choice: List[str]):
        super().action(choice)
        self.player.play_hand()


class AddCurseToDeck(MenuItem):
    def __init__(self, player: Player):
        super().__init__('Add curse to deck', player)

    def validate(self, choice: List[str]) -> bool:
        return len(choice) == 0

    def action(self, choice: List[str]):
        super().action(choice)
        self.player.add_curse('deck')


class AddCurseToHand(MenuItem):
    def __init__(self, player:Player):
        super().__init__('Add curse to hand', player)

    def validate(self, choice: List[str]) -> bool:
        return len(choice) == 0

    def action(self, choice: List[str]):
        super().action(choice)
        self.player.add_curse('hand')


class AddCurseToDiscard(MenuItem):
    def __init__(self, player:Player):
        super().__init__('Add curse to hand', player)

    def validate(self, choice: List[str]) -> bool:
        return len(choice) == 0

    def action(self, choice: List[str]):
        super().action(choice)
        self.player.add_curse('discard')

class DiscardToNumber(MenuItem):
    def __init__(self, player: Player):
        super().__init__(' [N] Discard to N cards', player)

    def validate(self, choice: List[str]) -> bool:
        if len(choice) != 1:
            print(f'Can only accept one additional argument, recieved {len(choice)}')
            return False
        the_choice = choice[0]
        try:
            the_choice = int(the_choice)
        except ValueError:
            print(f'Could not convert {the_choice} to an integer')
            return False

        if the_choice < 0:
            print(f'Cannot discard to {the_choice} cards!')
            return False
        return True
    
    def action(self, choice: List[str]):
        super().action(choice)
        discard_to = int(choice[0])
        self.player.deck.discard_to_n_cards(discard_to)


class DrawToNumber(MenuItem):
    def __init__(self, player: Player):
        super().__init__(' [N] Draw to N cards')
    
    def validate(self, choice: List[str]) -> bool:
        if len(choice) != 1:
            print(f'Can only accept one additional argument, recieved {len(choice)}')
            return False
        the_choice = choice[0]
        try:
            the_choice = int(the_choice)
        except ValueError:
            print(f'Could not convert {the_choice} to an integer')
            return False
        if the_choice < 0:
            print(f'Cannot add a negative number of cards! Told to add {the_choice}')
            return False
        return True

    def action(self, choice: List[str]):
        super().action(choice)
        add_until = int(choice[0])
        self.player.deck.draw_until_n_cards_in_hand(add_until)
        