import random


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.is_alive = True
        self.pending_turns = 1
        self.network = None
        self.adapter = None

    @property
    def defuse_cards_count(self):
        return len([card for card in self.hand if card.is_defuse])

    def get_playable_cards(self):
        return [card for card in self.hand if card.is_playable]

    @property
    def has_playable_cards_in_hand(self):
        return len(self.get_playable_cards()) > 0

    def pick_card(self, card):
        self.hand.append(card)

    def set_adapter(self, adapter):
        self.adapter = adapter

    def set_network(self, network):
        self.network = network

    def set_dead(self):
        self.is_alive = False

    def receive_card(self, card):
        self.hand.append(card)

    def receive_cards(self, cards):
        self.hand.extend(cards)

    @staticmethod
    def draw_card(deck):
        card = deck.draw_card()
        return card

    def play_card(self, card):
        self.hand.remove(card)

    def get_defuse_card(self):
        for card in self.hand:
            if card.is_defuse:
                return card

    def get_nope_card(self):
        for card in self.hand:
            if card.is_nope:
                return card

    def use_card(self, card):
        self.hand.remove(card)
        card.action()

    def place_exploding_kitten(self, card, deck):
        idx = self.decide_exploding_kitten_placement()
        deck.insert_card(idx, card)

    def decide_play_card(self):
        y = self.get_results()
        return y[0] > 0.5

    def decide_exploding_kitten_placement(self):
        y = self.get_results()
        return y[0]

    def decide_nope(self):
        y = self.get_results()
        return y[0] > 0.5

    def get_results(self):
        raise NotImplementedError


class RandomPlayer(Player):
    def get_results(self):
        return [random.random() for _ in range(8)]

    def choose_card(self):
        return random.choice(self.get_playable_cards())


class NeuralPlayer(Player):
    def get_results(self):
        return self.network.activate(self.adapter.input_array)
