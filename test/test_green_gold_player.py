import pytest

from dominion_ai.green_gold import GreenGoldPlayer
import dominion_ai.game as game

def test_can_make_player():
    the_game = game.make_std_game(4)
    gg = GreenGoldPlayer(the_game)


def test_initial_hand():
    the_game = game.make_std_game(4)
    gg = GreenGoldPlayer(the_game)
    assert len(gg.hand) == 5
    assert len(set(gg.hand)) <= 2

def test_discarding_cards():
    the_game = game.make_std_game(4, is_silent=True)
    gg = GreenGoldPlayer(the_game)

    gg.discard_card()
    gg.discard_card()

    assert len(gg.hand) == 3
    assert gg.hand_buying_power == 3
    assert len(set(gg.hand)) == 1

    gg.discard_card()
    gg.discard_card()

    assert len(gg.hand) == 1
    assert gg.hand_buying_power == 1

    gg.discard_card()
    gg.discard_card()
    gg.discard_card()
    assert len(gg.hand) == 0
