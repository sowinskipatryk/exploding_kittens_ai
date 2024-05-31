import random

from cards import Card
from deck import Deck
from players import Player, NeuralPlayer, RandomPlayer

from log.config import logger


class Game:
    def __init__(self, players_count=5):
        self.players_count = players_count
        self.players = [RandomPlayer(f"Player {i + 1}") for i in range(players_count)]
        self.deck = self.create_deck()

        self.deal_defuse_cards()
        self.deal_deck_cards()
        self.put_exploding_kittens_in_the_deck()
        self.shuffle_deck()

        self.current_player_index = random.randrange(0, players_count)
        self.turns_count = 1
        self.end_turn = False

    @property
    def alive_players_count(self):
        return len([player for player in self.players if player.is_alive])

    def shuffle_deck(self):
        self.deck.shuffle()

    def deal_defuse_cards(self):
        for player in self.players:
            player.receive_card(Card.Defuse())

    def deal_deck_cards(self, amount=7):
        for player in self.players:
            player.receive_cards([self.deck.draw_card() for _ in range(amount)])

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

        cards.extend([Card.Defuse() for _ in range(min(2, 6 - self.players_count))])

        deck = Deck(cards)
        return deck

    def put_exploding_kittens_in_the_deck(self):
        self.deck.cards.extend([Card.ExplodingKitten() for _ in range(self.players_count - 1)])

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
                logger.info(f"{current_player.name} [PLAY  ] Nope!")

        if len(nope_stack) % 2:
            return True

    def play(self):
        while self.alive_players_count > 1:
            logger.debug([player.is_alive for player in self.players])
            current_player = self.players[self.current_player_index]

            if not current_player.is_alive:
                logger.info(f"{current_player.name} [STATUS] dead")
                self.next_player()
                continue

            if not self.turns_count:
                self.next_player()
                self.turns_count = 1
                continue

            logger.info(f"{current_player.name} [STATUS] alive")
            logger.info(f"{current_player.name} [TURNS ] {self.turns_count}")
            logger.info(f"{current_player.name} [CARDS ] {current_player.hand}")

            while current_player.has_playable_cards_in_hand and current_player.decide_play_card() and not self.end_turn:
                played_card = current_player.choose_card()
                current_player.play_card(played_card)
                logger.info(f'{current_player.name} [PLAY  ] {played_card}')
                is_card_noped = self.resolve_nopes()
                if not is_card_noped:
                    logger.info(f'{current_player.name} [PLAY  ] {played_card} succeeded')
                    played_card.action(self)
                    if played_card.is_attack:
                        break

            if self.end_turn:
                self.end_turn = False
            else:
                drawn_card = current_player.draw_card(self.deck)

                logger.info(f'{current_player.name} [DRAW  ] {drawn_card}')

                if drawn_card.is_exploding_kitten:
                    drawn_card.action(self)
                else:
                    current_player.pick_card(drawn_card)

                self.turns_count -= 1

        winner = next(player for player in self.players if player.is_alive)
        logger.info(f"{winner.name} is the winner!")
