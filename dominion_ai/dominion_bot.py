from dominion_ai.game import make_std_game, make_prosperity_game
from dominion_ai.green_gold import GreenGoldPlayer
import fire

def start_the_game(n_players=2, prosperity=False,
                   has_curses=False, has_discard=False,
                   is_silent=False, late_game=3):
    greeting = f"""
    Welcome to Dominion bot:
      Configuration:
      --------------
      Players:       {n_players:2d}
      Game Type:     {'prosperity' if prosperity else 'standard'}
      Voice:         {not is_silent}
      Using curses?  {'yes' if has_curses else 'no'}
      "Late game"    {late_game} province in bots hand

      """
    print(greeting)
    if prosperity:
        game_fn = make_prosperity_game
    else:
        game_fn = make_std_game
    my_game = game_fn(n_players, is_silent, has_curses, has_discard)
    gg_player = GreenGoldPlayer(my_game, late_game)

    my_game.play_game(gg_player)

def main():
    fire.Fire(start_the_game)
