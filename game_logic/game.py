import random

from game_logic.cards import Card
from game_logic.deck import Deck
from game_logic.enums.card_names import CardName

from log.config import logger


class Game:
    def __init__(self, players):
        self.players_num = len(players)
        self.players = players

        self.deck = self.create_deck()

        self.deal_defuse_cards()
        self.shuffle_deck()
        self.deal_deck_cards()
        self.put_exploding_kittens_in_the_deck()
        self.shuffle_deck()

        self.current_player_index = random.randrange(0, self.players_num)
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
        self.current_player_index = (self.current_player_index + 1) % self.players_num

    def create_deck(self):
        cards = []
        cards += [Card.SeeTheFuture() for _ in range(5)]
        cards += [Card.Nope() for _ in range(5)]
        cards += [Card.Skip() for _ in range(4)]
        cards += [Card.Shuffle() for _ in range(4)]
        cards += [Card.Attack() for _ in range(4)]
        cards += [Card.Favor() for _ in range(4)]

        cards += [Card.BeardCat() for _ in range(4)]
        cards += [Card.TacoCat() for _ in range(4)]
        cards += [Card.HairyPotatoCat() for _ in range(4)]
        cards += [Card.Cattermelon() for _ in range(4)]
        cards += [Card.RainbowRalphingCat() for _ in range(4)]

        cards += [Card.Defuse() for _ in range(min(2, 6 - self.players_num))]

        deck = Deck(cards)
        return deck

    def put_exploding_kittens_in_the_deck(self):
        self.deck.cards.extend([Card.ExplodingKitten() for _ in range(self.players_num - 1)])

    def resolve_nopes(self):
        current_player_index = self.current_player_index
        nope_stack = []
        tries_since_nope = 0

        while tries_since_nope < self.players_num:
            tries_since_nope += 1
            current_player_index = (current_player_index + 1) % self.players_num
            current_player = self.players[current_player_index]

            nope_card = current_player.get_nope_card()
            if nope_card and current_player.decide_nope():
                current_player.play_card(nope_card, self)
                nope_stack.append(nope_card)
                tries_since_nope = 0
                logger.info(f"{current_player.name} [PLAY  ] Nope!")

        if len(nope_stack) % 2:
            return True

    def play(self):
        logger.info("GAME START")
        while self.alive_players_count > 1:
            current_player = self.players[self.current_player_index]

            if not current_player.is_alive:
                logger.debug(f"{current_player.name} [STATUS] dead")
                self.next_player()
                continue

            if not self.turns_count:
                self.next_player()
                self.turns_count = 1
                continue

            logger.debug(f"{current_player.name} [STATUS] alive")
            logger.debug(f"{current_player.name} [TURNS ] {self.turns_count}")
            logger.debug(f"{current_player.name} [CARDS ] {current_player.hand}")

            while current_player.has_playable_cards_in_hand and not self.end_turn:
                played_card = current_player.decide_play_card()
                if not played_card:
                    break
                current_player.play_card(played_card, self)
                logger.info(f'{current_player.name} [PLAY  ] {played_card}')
                is_card_noped = self.resolve_nopes()
                if not is_card_noped:
                    logger.info(f'{current_player.name} [PLAY  ] {played_card} succeeded')
                    played_card.action(self)
                    if played_card.is_attack:
                        break
                else:
                    logger.info(f'{current_player.name} [PLAY  ] {played_card} failed')

            if self.end_turn:
                self.end_turn = False
            else:
                drawn_card = current_player.draw_card(self.deck)

                logger.info(f'{current_player.name} [DRAW  ] {drawn_card}')

                if drawn_card.is_exploding_kitten:
                    drawn_card.action(self)
                else:
                    current_player.receive_card(drawn_card)

                logger.info(f'{current_player.name} [DECK  ] {self.deck.cards}')

                self.turns_count -= 1

        winner = next(player for player in self.players if player.is_alive)
        logger.info(f"{winner.name} [WINNER]")
        logger.info("GAME END")
