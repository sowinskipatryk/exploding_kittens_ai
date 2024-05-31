import random


class Deck:
    def __init__(self, cards):
        self.cards = cards

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()

    def insert_card(self, idx, card):
        self.cards.insert(idx, card)

    def __len__(self):
        return len(self.cards)
