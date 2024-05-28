import random

from cards import Card
from deck import Deck
from players import Player


class Game:
    def __init__(self, players_num):
        self.players_num = players_num
        self.players = [Player(f"Player {i + 1}") for i in range(players_num)]
        self.turn_index = random.randrange(0, players_num)
        self.deck = self.create_deck()
        self.deal_defuse_cards()

    def deal_defuse_cards(self):
        for player in self.players:
            player.get_card(Card.Defuse())

    def get_three_top_cards(self):
        return self.deck[-3:]

    def create_deck(self):
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

        cards.extend([Card.ExplodingKitten() for _ in range(self.players_num - 1)])
        cards.extend([Card.Defuse() for _ in range(min(2, 6 - self.players_num))])

        deck = Deck(cards)
        deck.shuffle()
        return deck

    def resolve_nope_stack(self, initial_player, card, game_state):
        nope_stack = []
        current_player_index = self.turn_index

        while True:
            current_player_index = (current_player_index + 1) % self.players_num
            current_player = game_state.players[current_player_index]

            if current_player != initial_player and current_player.has_card('Nope'):
                if current_player.wants_to_nope():
                    nope_card = current_player.play_nope()
                    nope_stack.append(nope_card)
                    print(f"{current_player.name} plays a Nope card!")

            if len(nope_stack) % 2 == 0:
                # Even number of Nopes, action goes through
                return False
            else:
                # Odd number of Nopes, action is noped
                if current_player_index == game_state.players.index(initial_player):
                    return True

    def play(self):
        turns_to_play = 1
        while len([player for player in self.players if player.is_alive]) > 1:
            if not turns_to_play:
                self.turn_index = (self.turn_index + 1) % len(self.players)

            current_player = self.players[self.turn_index]
            print(f"{current_player.name}'s turn")

            if current_player.is_alive:
                card = current_player.draw_card(self.deck)
                if card.is_exploding_kitten:
                    defuse_card = current_player.get_defuse_card()
                    if defuse_card:
                        current_player.use_card(defuse_card)
                    else:
                        current_player.set_dead()

        winner = next(player for player in self.players if player.is_alive)
        print(f"{winner.name} is the winner!")
