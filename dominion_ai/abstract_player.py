"""
Implements the abstract base class Player.

Different player classes differ by the different strategies they employ.
Currently playing actions is not supported, but different strategies can be
implmented by choosing how to
    - buy different cards during the buying phase
    - discarding cards during the "attack phase" of other players
"""
from abc import ABC, abstractmethod
from collections import Counter
from typing import List, Optional

import dominion_ai.cards as cards

from dominion_ai.utils import (
    speak_str,
    GameStage
)


class Player(ABC):
    def __init__(self, game, late_game_transition=3):
        """Start a player off with the default starting deck, an empty hand,
        and an empty discard pile.  Set the game stage to 'early_game'.
        Initialize a turn counter.  Draw a random starting hand from the
        deck."""

        self.game_stage = GameStage.early_game  # start the game in early stage
        self.deck = cards.Deck(player=self)
        self.game = game
        self.turn_count = 0
        self.late_game_transition = late_game_transition
        self.deck.draw_hand()  # start by drawing a hand

    def speak_hand(self):
        """Convenience function to generate a string describing the hand and
        speak it"""

        names_and_counts = Counter([c.name for c in self.hand]).most_common(
            len(self.hand)
        )

        s = "I have "
        s += " and ".join(
            [str(nac[1]) + " " + str(nac[0]) for nac in names_and_counts]
        )

        self.game.speak_str(s)

    @property
    def hand(self) -> List[cards.Card]:
        """Alias for the player's hand"""
        return self.deck.hand

    @property
    def victory_points(self) -> int:
        """Get the current victory points the bot has"""
        return self.deck.victory_points

    @property
    def hand_buying_power(self) -> int:
        """Gets the amount of money in hand (value)"""
        return self.deck.hand_buying_power

    @property
    def all_cards(self):
        return self.deck.all_cards

    @abstractmethod
    def buy_card(self) -> int:
        """Buys card according to strategy, returns number of cards bought"""
        pass

    @abstractmethod
    def discard_card(self) -> bool:
        pass

    @property
    def highest_buyable_money(self) -> Optional[cards.Card]:
        """Calculate the highest buyable money card"""
        bankroll = self.hand_buying_power
        # This list is sorted by buying power
        affordable_money_cards = [card for card in self.game.available_money
                                  if card.cost <= bankroll]
        if len(affordable_money_cards) > 0:
            return affordable_money_cards[0]
        return None

    @property
    def highest_buyable_victory_points(self) -> Optional[cards.Card]:
        """Calculate the highest buyable victory points card"""
        bankroll = self.hand_buying_power
        # This list is sorted by VP
        affordable_vp = [card for card in self.game.available_victory_points
                         if card.cost <= bankroll]
        if len(affordable_vp) > 0:
            return affordable_vp[0]
        return None

    def set_game_stage(self):
        """If the bot has 3 or more provinces, switch to late game stage,
        otherwise early game stage"""

        old_state = self.game_stage

        provinces_owned = len(
            [card for card in self.all_cards if card == cards.PROVINCE]
        )

        if provinces_owned < self.late_game_transition:
            self.game_stage = GameStage.early_game
        else:
            self.game_stage = GameStage.late_game
        if self.game_stage != old_state:
            s = f"Game Stage changed to {self.game_stage}"
            self.game.speak_str(s)

    def play_hand(self):
        """Play a hand: buy a card, re-evaluate the game stage, increment turn
        counter"""

        self.buy_card()
        self.set_game_stage()
        self.turn_count += 1

    def draw_hand(self):
        self.deck.draw_hand()

    def report(self):
        print(f"\tTurns so far: {self.turn_count}")
        print(f"\tVictory points so far: {self.victory_points}")
        print(f"\tAll cards: {Counter([c.name for c in self.all_cards])}")
        print(f"\t\tHand: {Counter([c.name for c in self.hand])}")
        print(f"\t\tDiscard: {Counter([c.name for c in self.deck.discard])}")
        print(f"\t\tDeck: {Counter([c.name for c in self.deck.deck])}")

    def add_curse(self, where: str='discard'):
        where_dict = {
            'hand': self.deck.hand,
            'discard': self.deck.discard,
            'draw': self.deck.deck
        }
        try:
            where_dict[where].append(cards.CURSE)
        except KeyError as e:
            print(f'Told to add curse {where}, should be one of {where_dict.keys()}')
            raise e
