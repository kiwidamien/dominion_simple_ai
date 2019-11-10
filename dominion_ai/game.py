from enum import Enum
from typing import Dict, List, Optional

from dominion_ai.cards import (
    Card,
    COLONY,
    PROVINCE,
    DUCKY,
    ESTATE,
    PLATINUM,
    GOLD,
    SILVER,
    COPPER
)
from dominion_ai.utils import speak_str


class GameStage(Enum):
    """Game Stage is used to affect behavior depending on where in the game the
    player is"""

    early_game = 1
    late_game = 2


class Game:
    def __init__(self, available_cards: Dict[Card, Optional[int]],
                 is_silent=False, has_attack_cards=False):
        self.limited_card_types = {c: amt for c, amt in available_cards.items()
                                    if amt is not None}
        self.unlimited_card_types = [c for c, amt in available_cards.items()
                                    if amt is not None]
        if PROVINCE not in self.limited_card_types:
            msg = f"""Dominion requires Provinces for its end condition,
                     received {available_cards}
                     (no providences)"""
            raise ValueError(msg)
        self.is_silent = is_silent
        self.has_attack = has_attack_cards

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

    @property
    def available_money(self) -> List[Card]:
        available_money = [card for card in self.available_cards if card.buying_power > 0]
        return sorted(available_money, key=lambda card: card.buying_power, ascending=False)

    @property
    def available_victory_points(self) -> List[Card]:
        available_vp = [card for card in self.available_cards if card.victory_points > 0]
        return sorted(available_vp, key=lambda card: card.victory_points, ascending=False)

    @property
    def number_of_providences_remaining(self) -> int:
        return self.limited_card_types[PROVINCE]

    def speak_str(s):
        speak_str(s, self.is_silent)


STD_GAME_CARDS = {
    ESTATE: None,
    DUCKY: None,
    PROVINCE: None,
    COPPER: None,
    SILVER: None,
    GOLD: None
}

PROSPERITY_GAME_CARDS = {
    **STD_GAME_CARDS,
    COLONY: None,
    PLATINUM: None
}

def get_vp_pile_size(num_players: int) -> int:
    if num_players == 2:
        return 8
    if num_palyers == 3:
        return 12
    return 3 * num_players

def make_std_game(num_players):
    std_game = STD_GAME_CARDS.copy()
    std_game[PROVINCE] = get_vp_pile_size(num_players)
    return Game(std_game)

def make_prosperity_game(num_players):
    prosp_game = PROSPERITY_GAME_CARDS.copy()
    prosp_game[PROVINCE] = get_vp_pile_size(num_players)
    prosp_game[COLONY] = get_vp_pile_size(num_players)
    return Game(prosp_game)
