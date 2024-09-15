import random

from log.config import logger


class Deck:
    def __init__(self, cards):
        self.cards = cards

    def shuffle(self):
        logger.debug('shuffle')
        logger.debug(f"cards before {self.cards}")
        random.shuffle(self.cards)
        logger.debug(f"cards after {self.cards}")

    def draw_card(self):
        card = self.cards.pop()
        print(card)
        logger.debug(f"draw_card {card}")
        logger.debug(f"cards after {self.cards}")
        return card

    def insert_card(self, idx, card):
        self.cards.insert(idx, card)
        logger.debug(f"insert_card {card} at index {idx}")
        logger.debug(f"cards after {self.cards}")

    def get_top_three_cards(self):
        return self.cards[-3:]

    def __len__(self):
        return len(self.cards)
