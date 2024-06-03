import random

from log.config import logger


class Deck:
    def __init__(self, cards):
        self.cards = cards

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        logger.debug(f"draw_card {self.cards}")
        return self.cards.pop()

    def insert_card(self, idx, card):
        self.cards.insert(idx, card)
        logger.debug(f"insert_card {self.cards}")

    def get_top_three_cards(self):
        return self.cards[-3:]

    def __len__(self):
        return len(self.cards)
