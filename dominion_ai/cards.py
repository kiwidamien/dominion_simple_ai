from collections import namedtuple
import random
from typing import List

# Define the cards in the game
Card = namedtuple("Card", "name cost buying_power victory_points only_prosperity")

# victory point cards (base game)
CURSE = Card(name="curse", cost=0, buying_power=0, victory_points=-1, only_prosperity=False)
ESTATE = Card(name="estate", cost=2, buying_power=0, victory_points=1, only_prosperity=False)
DUCKY = Card(name="duchy", cost=5, buying_power=0, victory_points=3, only_prosperity=False)
PROVINCE = Card(name="province", cost=8, buying_power=0, victory_points=6, only_prosperity=False)

# money cards (base game)
COPPER = Card(name="copper", cost=0, buying_power=1, victory_points=0, only_prosperity=False)
SILVER = Card(name="silver", cost=3, buying_power=2, victory_points=0, only_prosperity=False)
GOLD = Card(name="gold", cost=6, buying_power=3, victory_points=0, only_prosperity=False)

# For playing with the Prosperity expansion, add colony and platinum
COLONY = Card(name="colony", cost=11, buying_power=0, victory_points=10, only_prosperity=True)
PLATINUM = Card(name="platinum", cost=9, buying_power=5, victory_points=0, only_prosperity=True)


class Deck:
    def __init__(self, player):
        self.deck = 3*[ESTATE] + 7*[COPPER]
        self.discard = []
        self.hand = []
        random.shuffle(self.deck)
        self.player = player

    def draw_card(self) -> bool:
        if (len(self.deck) == 0) and (len(self.discard) == 0):
            # we are out of cards
            return False
        if len(self.deck) == 0:
            random.shuffle(self.discard)
            self.deck, self.discard = self.discard, self.deck
        # Move a card from the deck to the hand
        self.hand.append(self.deck.pop())
        return True

    def discard_card(self) -> bool:
        return self.player.discard_card()

    def discard_hand(self):
        self.discard = self.discard + self.hand
        self.hand = []

    @property
    def all_cards(self) -> List[Card]:
        return self.hand + self.discard + self.deck

    @property
    def cards_in_hand(self):
        return len(self.hand)

    @property
    def hand_buying_power(self) -> int:
        return sum([c.buying_power for c in self.hand])

    @property
    def victory_points(self) -> int:
        return sum([c.victory_points for c in self.hand])

    def draw_hand(self, n_cards: int=5) -> bool:
        """Draws a new hand of n_cards.

        Returns True if the operation was successful (i.e. we were able to draw
        n_cards into a hand), False otherwise. Raises AttributeError if hand is
        not already empty.
        """
        if len(self.hand) != 0:
            raise AttributeError(f'Hand should be empty! Instead contains {self.hand}')
        self.draw_until_n_cards_in_hand(n_cards)

    def draw_until_n_cards_in_hand(self, n_cards: int) -> bool:
        """Draw cards into hand, until we have n_cards in hand or are out of cards.

        Does not require hand to be empty. Does not discard cards.
        """
        while len(self.hand) < n_cards:
            if not self.draw_card():
                return False
        return True

    def draw_n_more_cards(self, n_cards: int) -> sum:
        return sum([self.draw_card() for _ in range(n_cards)])

    def discard_to_n_cards(self, n_cards: int) -> bool:
        # We cannot end with n_cards
        if len(self.hand) < n_cards:
            return False
        while len(self.hand) > n_cards:
            self.discard_card()
        return True

    def discard_up_to_n_cards(self, n_cards: int) -> int:
        return sum([self.discard_card() for _ in range(n_cards)])
