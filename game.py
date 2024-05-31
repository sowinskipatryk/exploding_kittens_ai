import random

from cards import Card
from deck import Deck
from players import Player, NeuralPlayer, RandomPlayer


class Game:
    def __init__(self, players_count):
        self.players_count = players_count
        self.players = [RandomPlayer(f"Player {i + 1}") for i in range(players_count)]
        self.deck = self.create_deck()
        self.deal_defuse_cards()

        self.current_player_index = random.randrange(0, players_count)
        self.turns_count = 1
        self.skip_draw = False

    @property
    def alive_players_count(self):
        return len([player for player in self.players if player.is_alive])

    def deal_defuse_cards(self):
        for player in self.players:
            player.receive_card(Card.Defuse())

    def get_three_top_cards(self):
        return self.deck[-3:]

    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % self.players_count

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

        cards.extend([Card.ExplodingKitten() for _ in range(self.players_count - 1)])
        cards.extend([Card.Defuse() for _ in range(min(2, 6 - self.players_count))])

        deck = Deck(cards)
        deck.shuffle()
        return deck

    def resolve_nopes(self):
        current_player_index = self.current_player_index
        nope_stack = []
        tries_since_nope = 0

        while tries_since_nope < self.players_count:
            tries_since_nope += 1
            current_player_index = (current_player_index + 1) % self.players_count
            current_player = self.players[current_player_index]

            nope_card = current_player.get_nope_card()
            if nope_card and current_player.decide_nope():
                current_player.play_card(nope_card)
                nope_stack.append(nope_card)
                tries_since_nope = 0
                print(f"{current_player.name} plays a Nope card!")

        if len(nope_stack) % 2 == 0:
            return True

    def play(self):
        while self.alive_players_count > 1:
            current_player = self.players[self.current_player_index]

            if not current_player.is_alive:
                self.next_player()
                continue

            if not self.turns_count:
                self.next_player()
                self.turns_count = 1
                continue

            print(f"{current_player.name}'s turn")

            attack = False
            while current_player.has_cards_in_hand and current_player.decide_play_card() and not attack:
                play_card = current_player.choose_card()
                is_card_noped = self.resolve_nopes()
                if not is_card_noped:
                    play_card.use()
                    print(f'{play_card} is used!')
                    if play_card.is_attack:
                        attack = True

            if attack:
                continue

            if self.skip_draw:
                self.skip_draw = False
            else:
                card = current_player.draw_card(self.deck)

                if card.is_exploding_kitten:
                    card.use(self)
                    # defuse_card = current_player.get_defuse_card()
                    # if defuse_card:
                    #     current_player.use_card(defuse_card)
                    # else:
                    #     current_player.set_dead()

            self.turns_count -= 1

        winner = next(player for player in self.players if player.is_alive)
        print(f"{winner.name} is the winner!")
