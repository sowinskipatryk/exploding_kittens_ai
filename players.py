import random


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

    def set_dead(self):
        self.is_alive = False

    def get_card(self, card):
        self.hand.append(card)

    def draw_card(self, deck):
        card = deck.draw_card()
        self.hand.append(card)
        return card

    def play_card(self, card):
        self.hand.remove(card)

    def get_defuse_card(self):
        for card in self.hand:
            if card.is_defuse:
                return card

    def use_card(self, card):
        self.hand.remove(card)
        card.use()

    def place_exploding_kitten(self, card, deck):
        idx = self.decide_exploding_kitten_placement()
        deck.put_card(idx, card)

    def decide_play_card(self):
        y = self.get_results()
        if y[0] > 0.5:
            return True

    def decide_exploding_kitten_placement(self):
        y = self.get_results()
        return y[0]

    def get_results(self):
        raise NotImplementedError


class RandomPlayer(Player):
    def get_results(self):
        return [random.random() for _ in range(100)]


class NeuralPlayer(Player):
    def get_results(self):
        return self.network.activate(self.adapter.input_array)
