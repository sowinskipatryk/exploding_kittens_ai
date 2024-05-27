import random

from cards import Card
from deck import Deck
from players import Player


class Game:
    def __init__(self, num_players):
        self.turn_index = random.randrange(0, num_players)
        self.deck = self.create_deck(num_players)
        self.players = [Player(f"Player {i + 1}") for i in range(num_players)]
        self.deal_defuse_cards()

    def deal_defuse_cards(self):
        for player in self.players:
            player.get_card(Card.Defuse())

    @staticmethod
    def create_deck(num_players):
        cards = []
        cards.extend([Card.SeeTheFuture() for _ in range(5)])
        cards.extend([Card.Nope() for _ in range(5)])
        cards.extend([Card.Skip() for _ in range(4)])
        cards.extend([Card.Shuffle() for _ in range(4)])
        cards.extend([Card.Attack() for _ in range(4)])
        cards.extend([Card.Favor() for _ in range(4)])

        cards.extend([Card.BeardCat() for _ in range(4)])
        cards.extend([Card.TacoCat() for _ in range(4)])
        cards.extend([Card.HairyPotatoCat() for _ in range(4)])
        cards.extend([Card.Cattermelon() for _ in range(4)])
        cards.extend([Card.RainbowRalphingCat() for _ in range(4)])

        cards.extend([Card.ExplodingKitten() for _ in range(num_players - 1)])
        cards.extend([Card.Defuse() for _ in range(min(2, 6 - num_players))])

        deck = Deck(cards)
        deck.shuffle()
        return deck

    def play(self):
        while len([player for player in self.players if player.is_alive]) > 1:
            current_player = self.players[self.turn_index]
            if current_player.is_alive:
                print(f"{current_player.name}'s turn:")
                if current_player.decide_play_card():
                    # do action
                    card = current_player.draw_card(self.deck)


                # if current_player.pending_turns > 0:
                    # self.last_played_card = None
                    if action.lower() == 'draw':

                        current_player.pending_turns -= 1
                    else:
                        result = current_player.play_card(action, self.deck, self.players, self.last_played_card)
                        if result == 'NOPE':
                            continue
                        elif result:
                            self.last_played_card = result
                else:
                    print(f"{current_player.name} skips their turn due to pending actions.")

            self.turn_index = (self.turn_index + 1) % len(self.players)

        winner = next(player for player in self.players if player.is_alive)
        print(f"{winner.name} is the winner!")
