from dominion_ai.abstract_player import Player
from dominion_ai.game import GameStage
import dominion_ai.cards as cards


class GreenGoldPlayer(Player):
    def buy_card(self):
            """Implement the "greens and golds" strategy of buying the highest
            victory point card (in the game) if possible, and otherwise buying the
            highest buyable money card (though never buying coppers).  If >3 of the
            highest victory point card are owned, then switch to "late_game"
            strategy and just buy the highest buyable victory points.  After using
            the hand to buy a card (or not), discard the rest of the hand."""

            print(f"Hand has buying power {self.hand_buying_power}...")

            # if ever (game stage agnostic) can buy a province or colony, always buy it
            if ((self.highest_buyable_victory_points == cards.PROVINCE) or
                (self.highest_buyable_victory_points == cards.COLONY)):
                bought_card = self.highest_buyable_victory_points
            else:
                # buy the highest buyable money by default
                if (self.highest_buyable_money != cards.COPPER):
                    bought_card = self.highest_buyable_money

            # except if in the late game stage, in which case buy the highest
            # buyable victory points instead
            if ((self.game_stage == GameStage.late_game) and
                (self.self.highest_buyable_victory_points.victory_points > 0)):
                bought_card = self.highest_buyable_victory_points
                print(f"Late Stage Game, so buying victory points over money")

            # explain the play
            self.speak_hand()
            s = f"for total buying power of {self.hand_buying_power}"
            self.game.speak_str(s)

            # gain the card bought, if any, to the discard pile:
            if bought_card:
                s = f"I buy {bought_card.name}"
                self.game.speak_str(s)

                # gain the card to the discard pile
                self.discard.append(bought_card)
            else:
                s = f"I do not buy anything"
                self.game.speak_str(s)

            # the whole hand is used up buying the card, discard the hand
            for card in self.hand:
                self.discard.append(card)

    def discard_card(self):
        if len(self.deck.hand) == 0:
            return False
        # be willing to discard of expensive cards that don't contribute to buying power
        self.hand = sorted(self.deck.hand, key=lambda card: (-card.buying_power, card.victory_points))
        my_card = self.deck.hand.pop()
        self.deck.discard.append(my_card)
        self.game.speak_str(f'Discarded {my_card}')
        return True
