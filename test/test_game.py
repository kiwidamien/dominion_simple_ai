import pytest
import dominion_ai.game as game


def test_create_std_game():
    game.make_std_game(4)


def test_create_prosperity_game():
    game.make_prosperity_game(5)


def test_game_can_be_created_with_limited_nonzero_provinces():
    cards = {
        game.ESTATE: None,
        game.PROVINCE: 8
    }
    g = game.Game(cards)


def test_game_raises_ValueError_with_infinite_provinces():
    with pytest.raises(ValueError):
        cards = {
            game.ESTATE: None,
            game.PROVINCE: None
        }
        g = game.Game(cards)


def test_game_raises_ValueError_with_no_provinces():
    with pytest.raises(ValueError):
        cards = {
            game.ESTATE: None,
            game.DUCKY: None,
            game.COLONY: 40
        }
        g = game.Game(cards)


def test_std_game_has_gold_silver_copper():
    g = game.make_std_game(4)
    assert g.available_money == [game.GOLD, game.SILVER, game.COPPER]


def test_std_game_has_right_vp_cards():
    g = game.make_std_game(4)
    assert g.available_victory_points == [game.PROVINCE, game.DUCKY, game.ESTATE]


def test_prosperity_game_has_right_money():
    g = game.make_prosperity_game(5)
    assert g.available_money == [game.PLATINUM, game.GOLD, game.SILVER, game.COPPER]


def test_prosperity_game_has_right_vp_cards():
    g = game.make_prosperity_game(5)
    assert g.available_victory_points == [game.COLONY, game.PROVINCE, game.DUCKY,
                                          game.ESTATE]
