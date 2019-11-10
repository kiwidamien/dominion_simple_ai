import dominion_ai.cards as cards
from dominion_ai.game import (
    GameStage
)


class Player:
    def __init__(self):
        """Start a player off with the default starting deck, an empty hand,
        and an empty discard pile.  Set the game stage to 'early_game'.
        Initialize a turn counter.  Draw a random starting hand from the
        deck."""

        self.game_stage = GameStage.early_game  # start the game in early stage
        self.deck = cards.Deck(player=self)
        self.turn_count = 0
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

        speak_str(s)

    def buy_card(self):
        """Implement the "greens and golds" strategy of buying the highest
        victory point card (in the game) if possible, and otherwise buying the
        highest buyable money card (though never buying coppers).  If >3 of the
        highest victory point card are owned, then switch to "late_game"
        strategy and just buy the highest buyable victory points.  After using
        the hand to buy a card (or not), discard the rest of the hand."""

        print(f"Hand has buying power {self.hand_buying_power}...")

        # if ever (game stage agnostic) can buy a province, always buy it
        if self.highest_buyable_victory_points == province:
            bought_card = self.highest_buyable_victory_points
        else:
            # buy the highest buyable money by default
            bought_card = self.highest_buyable_money

        # except if in the late game stage, in which case buy the highest
        # buyable victory points instead
        if self.game_stage == GameStage.late_game:
            bought_card = self.highest_buyable_victory_points
            print(f"Late Stage Game, so buying victory points over money")

        # explain the play
        self.speak_hand()
        s = f"for total buying power of {self.hand_buying_power}"
        speak_str(s)

        # gain the card bought, if any, to the discard pile:
        if bought_card:
            s = f"I buy {bought_card.name}"
            speak_str(s)

            # gain the card to the discard pile
            self.discard.append(bought_card)
        else:
            s = f"I do not buy anything"
            speak_str(s)

        # the whole hand is used up buying the card, discard the hand
        for card in self.hand:
            self.discard.append(card)
        self.hand = []

    def discard_card(self) -> bool:
        return True

    @property
    def highest_buyable_money(self):
        """Calculate the highest buyable money card"""

        # Prosperity expansion:
        # if self.hand_buying_power >= 9:
        #     return platinum

        if self.hand_buying_power >= 6:
            return gold
        elif self.hand_buying_power >= 3:
            return silver
        else:
            return None  # don't buy coppers

    @property
    def highest_buyable_victory_points(self):
        """Calculate the highest buyable victory points card"""

        # Prosperity expansion:
        # if self.hand_buying_power >= 11:
        #     return colony

        if self.hand_buying_power >= 8:
            return province
        elif self.hand_buying_power >= 5:
            return duchy
        elif self.hand_buying_power >= 2:
            return estate
        else:
            return None


    @property
    def victory_points(self):
        """Get the current victory points the bot has"""
        return self.deck.victory_points

    def set_game_stage(self):
        """If the bot has 3 or more provinces, switch to late game stage,
        otherwise early game stage"""

        provinces_owned = len(
            [card for card in self.all_cards if card == province]
        )

        if provinces_owned < 3:
            self.game_stage = GameStage.early_game
        else:
            self.game_stage = GameStage.late_game
            s = f"Game Stage changed to {self.game_stage}"
            speak_str(s)

    def play_hand(self):
        """Play a hand: buy a card, re-evaluate the game stage, increment turn
        counter"""

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
