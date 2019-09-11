from enum import Enum
from collections import namedtuple
import random
from collections import Counter


# Define the cards in the game
Card = namedtuple("Card", "name cost buying_power victory_points")
estate = Card(name="estate", cost=2, buying_power=0, victory_points=1)
duchy = Card(name="duchy", cost=5, buying_power=0, victory_points=3)
province = Card(name="province", cost=8, buying_power=0, victory_points=6)
copper = Card(name="copper", cost=0, buying_power=1, victory_points=0)
silver = Card(name="silver", cost=3, buying_power=2, victory_points=0)
gold = Card(name="gold", cost=6, buying_power=3, victory_points=0)


class GameStage(Enum):
    early_game = 1
    late_game = 2


class Player:
    def __init__(self):
        self.hand = []  # empty hand
        self.discard = []  # empty discard pile
        self.deck = 3 * [estate] + 7 * [copper]  # starting hand
        self.game_stage = GameStage.early_game  # start the game in early stage
        self.turn_count = 0

        random.shuffle(
            self.deck
        )  # shuffle the deck before drawing (first time)
        self.draw_hand()  # start by drawing a hand

    def draw_hand(self, to_n_in_hand=5):
        while len(self.hand) < to_n_in_hand:  # draw until n in hand
            self.draw_card()
        print(f"Drawing new hand: {Counter([c.name for c in self.hand])}")

    def draw_card(self):

        if len(self.deck) == 0:  # if the deck has no cards
            random.shuffle(self.discard)  # shuffle discard
            self.deck = self.discard  # discard becomes deck
            self.discard = []  # discard is now empty

        card = self.deck.pop()  # draw a card from the deck

        self.hand.append(card)  # add the card to the hand

    def buy_card(self):
        print(f"Hand has buying power {self.hand_buying_power}...")

        # if ever (game stage agnostic) can buy a province, always buy it
        if self.can_buy_province:
            bought_card = province

        else:
            # buy the highest buyable money by default
            bought_card = self.highest_buyable_money

            # except if in the late game stage, in which case buy the highest
            # buyable victory points instead
            if self.game_stage == GameStage.late_game:
                bought_card = self.highest_buyable_victory_points
                print(f"Late Stage Game, so buying victory points over money")

        # gain the card bought, if any, to the discard pile:
        if bought_card:
            print(f"Buying card: {bought_card.name}")
            self.discard.append(bought_card)

        # the whole hand is used up buying the card
        for card in self.hand:
            self.discard.append(card)
        self.hand = []

    @property
    def hand_buying_power(self):
        return sum([card.buying_power for card in self.hand])

    @property
    def highest_buyable_money(self):
        if self.hand_buying_power >= 6:
            return gold
        elif self.hand_buying_power >= 3:
            return silver
        else:
            return None  # don't buy coppers

    @property
    def highest_buyable_victory_points(self):
        if self.hand_buying_power >= 8:
            return province
        elif self.hand_buying_power >= 5:
            return duchy
        elif self.hand_buying_power >= 2:
            return estate
        else:
            return None

    @property
    def can_buy_province(self):
        return self.highest_buyable_victory_points == province

    @property
    def all_cards(self):
        return self.hand + self.deck + self.discard

    @property
    def provinces_owned(self):
        return len([card for card in self.all_cards if card == province])

    @property
    def victory_points(self):
        return sum([card.victory_points for card in self.all_cards])

    def set_game_stage(self):
        provinces_owned = len(
            [card for card in self.all_cards if card == province]
        )

        if provinces_owned < 3:
            self.game_stage = GameStage.early_game
        else:  # provinces_owned >= 3
            self.game_stage = GameStage.late_game
            print(f"Game Stage changed to {self.game_stage}")

    def play_hand(self):

        self.buy_card()

        # set the GameStage (might or might not change)
        self.set_game_stage()

        self.turn_count += 1

    def report(self):
        print(f"\tTurns so far: {self.turn_count}")
        print(f"\tVictory points so far: {self.victory_points}")
        print(f"\tAll cards: {Counter([c.name for c in self.all_cards])}")
        print(f"\t\tHand: {Counter([c.name for c in self.hand])}")
        print(f"\t\tDiscard: {Counter([c.name for c in self.discard])}")
        print(f"\t\tDeck: {Counter([c.name for c in self.deck])}")


if __name__ == "__main__":
    print(f"Starting a new game\n")

    p = Player()
    p.report()

    while True:
        _ = input("\nPress Enter to take a turn...\n")
        p.play_hand()
        p.draw_hand()
        p.report()
