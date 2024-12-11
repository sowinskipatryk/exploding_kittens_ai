import random

from game_logic.cards import (Defuse, SeeTheFuture, Nope, Skip, Shuffle, Attack, Favor, BeardCat, TacoCat,
                              HairyPotatoCat, Cattermelon, RainbowRalphingCat, ExplodingKitten)
from log.config import logger


class Deck:
    def __init__(self, players_num):
        self._players_num = players_num
        self.cards = self._create_deck()

    def _create_deck(self):
        deck = []

        # Single cards
        deck += [Defuse() for _ in range(min(2, 6 - self._players_num))]
        deck += [SeeTheFuture() for _ in range(5)]
        deck += [Nope() for _ in range(5)]
        deck += [Skip() for _ in range(4)]
        deck += [Shuffle() for _ in range(4)]
        deck += [Attack() for _ in range(4)]
        deck += [Favor() for _ in range(4)]

        # Pair cards
        deck += [BeardCat() for _ in range(4)]
        deck += [TacoCat() for _ in range(4)]
        deck += [HairyPotatoCat() for _ in range(4)]
        deck += [Cattermelon() for _ in range(4)]
        deck += [RainbowRalphingCat() for _ in range(4)]

        return deck

    def shuffle(self):
        logger.debug(f"[Deck] cards before shuffle {self.cards}")
        random.shuffle(self.cards)
        logger.debug(f"[Deck] cards after shuffle {self.cards}")

    def get_card(self):
        card = self.cards.pop()
        logger.debug(f"[Deck] draw card {card}")
        logger.debug(f"[Deck] cards after draw {self.cards}")
        return card

    def insert_card(self, pos, card):
        self.cards.insert(pos, card)
        logger.debug(f"[Deck] insert card {card} at index {pos}")
        logger.debug(f"[Deck] cards after insertion {self.cards}")

    def check_three_top_cards(self):
        top_cards = self.cards[:-4:-1]
        logger.debug(f"[Deck] check three top cards {top_cards}")
        return top_cards

    def __len__(self):
        return len(self.cards)

    @staticmethod
    def get_initial_defuse_card():
        return Defuse()

    def insert_exploding_kittens(self):
        self.cards.extend([ExplodingKitten() for _ in range(self._players_num - 1)])
        logger.debug(f"[Deck] cards after insertion {self.cards}")

    def insert_remaining_defuse_cards(self):
        self.cards.extend([Defuse() for _ in range(min(2, 6 - self._players_num))])
        logger.debug(f"[Deck] cards after insertion {self.cards}")
