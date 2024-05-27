from enum import Enum


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.is_alive = True
        self.pending_turns = 1
        self.network = None
        self.adapter = None

    def set_adapter(self, adapter):
        self.adapter = adapter

    def set_network(self, network):
        self.network = network

    def get_card(self, card):
        self.hand.append(card)

    def draw_card(self, deck):
        card = deck.draw()
        self.hand.append(card)

    @property
    def get_defuse_cards(self):
        return [card for card in self.hand if card.is_defuse]

    def decide_play_card(self):
        y = self.network.activate(self.adapter.input_array)
        if y > 0.5:
            return True
