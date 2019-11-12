from dominion_ai.game import make_std_game, make_prosperity_game
from dominion_ai.green_gold import GreenGoldPlayer


def main():
    print("Hello from dominion_bot")
    my_game = make_std_game(2)
    my_game = make_prosperity_game(2)
    gg_player = GreenGoldPlayer(my_game)

    while True:
        _ = input("\nPress Enter to take a turn...\n")
        gg_player.report()
        gg_player.play_hand()
        gg_player.draw_hand()

if __name__ == '__main__':
    main()
