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
from dominion_ai.abstract_player import Player
from dominion_ai.menu import (
    Menu,
    DEFAULT_MENU,
    DRAW_DISCARD_MENU,
    DRAW_DISCARD_CURSE_MENU
)


class Game:
    def __init__(self, available_cards: Dict[Card, Optional[int]],
                 menu: Menu=DEFAULT_MENU,
                 is_silent: bool=False, has_attack_cards: bool=False):
        self.limited_card_types = {c: amt for c, amt in available_cards.items()
                                    if amt is not None}
        self.unlimited_card_types = [c for c, amt in available_cards.items()
                                    if amt is None]
        if PROVINCE not in self.limited_card_types:
            msg = f"""Dominion requires Provinces for its end condition,
                     received {available_cards}
                     (no providences)"""
            raise ValueError(msg)
        self.is_silent = is_silent
        self.has_attack = has_attack_cards
        self.menu = menu

    def set_is_silent(self, silence_flag: bool):
        self.is_silent = silence_flag

    @property
    def available_cards(self) -> List[Card]:
        return ([c for c, amt in self.limited_card_types.items() if amt > 0]
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
        return sorted(available_money, key=lambda card: card.buying_power, reverse=True)

    @property
    def available_victory_points(self) -> List[Card]:
        available_vp = [card for card in self.available_cards if card.victory_points > 0]
        return sorted(available_vp, key=lambda card: card.victory_points, reverse=True)

    @property
    def number_of_providences_remaining(self) -> int:
        return self.limited_card_types[PROVINCE]

    def speak_str(self, s):
        speak_str(s, self.is_silent)

    def _do_round(self, player:Player):
        self.menu.do_round(player)

    def play_game(self, player: Player):
        while True:
            player.report()
            self._do_round(player)
            player.draw_hand()


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
    if num_players == 3:
        return 12
    return 3 * num_players


def get_menu(has_curses, has_discard):
    if has_curses:
        return DRAW_DISCARD_CURSE_MENU
    if has_discard:
        return DRAW_DISCARD_MENU
    return DEFAULT_MENU


def make_std_game(num_players, is_silent=False, has_curses=False,
                  has_discard=False):
    std_game = STD_GAME_CARDS.copy()
    std_game[PROVINCE] = get_vp_pile_size(num_players)
    return Game(std_game, is_silent=is_silent,
                menu=get_menu(has_curses, has_discard))


def make_prosperity_game(num_players, is_silent=False, has_curses=False,
                         has_discard=False):
    prosp_game = PROSPERITY_GAME_CARDS.copy()
    prosp_game[PROVINCE] = get_vp_pile_size(num_players)
    prosp_game[COLONY] = get_vp_pile_size(num_players)
    return Game(prosp_game, is_silent=is_silent,
                menu=get_menu(has_curses, has_discard))
