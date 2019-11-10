from enum import Enum
from typing import Dict, List, Optional

from dominion_ai.cards import Card


class GameStage(Enum):
    """Game Stage is used to affect behavior depending on where in the game the
    player is"""

    early_game = 1
    late_game = 2

def Game:
    def __init__(self, available_cards: Dict[Card, Optional[int]]):
        self.limited_card_types = {c: amt for c, amt in available_cards.items()
                                    if amt is not None}
        self.unlimited_card_types = [c for c, amt in available_cards.items()
                                    if amt is not None]

    @property
    def available_cards(self) -> List[Card]:
        return ([c for c, amt in self.limited_card_types if amt > 0]
                + self.unlimited_card_types)

    def buy_card(self, card_to_buy: Card):
        if card_to_buy not in self.available_cards:
            msg = f'''Tried to buy {card_to_buy}, but there are none available!'''
            raise ValueError(msg)
        if card_to_buy in self.limited_card_types:
            self.limited_card_types[card_to_buy] -= 1
