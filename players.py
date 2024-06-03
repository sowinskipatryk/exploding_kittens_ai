import random

from mapping import CARDS_MAPPING


class Player:
    def __init__(self, index):
        self.index = index
        self.name = f"Player {index + 1}"
        self.hand = []
        # self.top_three_deck_cards = []
        self.is_alive = True
        self.network = None
        self.adapter = None

    @property
    def defuse_cards_count(self):
        return len([card for card in self.hand if card.is_defuse])

    def get_playable_cards(self):
        return [card for card in self.hand if card.is_playable()]

    def get_cards_in_hand_filter(self):
        hand_types = [type(card) for card in self.hand]
        return [1 if card in hand_types else 0 for card in CARDS_MAPPING]

    def has_multiple_cards_of_type(self, card_type, amount):
        return len([card for card in self.hand if isinstance(card, card_type)]) > amount

    @property
    def has_playable_cards_in_hand(self):
        return len(self.get_playable_cards()) > 0

    def receive_card(self, card):
        self.hand.append(card)
        self.update_playable_cards()

    def receive_cards(self, cards):
        self.hand.extend(cards)
        self.update_playable_cards()

    def update_playable_cards(self):
        pass

    def set_adapter(self, adapter):
        self.adapter = adapter

    def set_network(self, network):
        self.network = network

    def set_dead(self):
        self.is_alive = False

    def get_from_hand(self, card):
        self.hand.remove(card)

    @staticmethod
    def draw_card(deck):
        card = deck.draw_card()
        return card

    def play_card(self, card, game):
        self.get_from_hand(card)
        card.action(game)
        self.update_playable_cards()

    def get_defuse_card(self):
        for card in self.hand:
            if card.is_defuse:
                return card

    def get_nope_card(self):
        for card in self.hand:
            if card.is_nope:
                return card

    def correct_opponent_index(self, opp_id):
        if self.index > opp_id:
            return opp_id + 1
        return opp_id

    def place_exploding_kitten(self, card, deck):
        idx = self.decide_exploding_kitten_placement()
        deck.insert_card(idx, card)

    def decide_play_card(self):
        y = self.get_results()
        print(CARDS_MAPPING)
        cards_values = y[:12]
        print(cards_values)
        cards_filter = self.get_cards_in_hand_filter()
        print(cards_filter)
        filtered_values = [value if cards_filter[i] else 0 for i, value in enumerate(cards_values)]
        print(filtered_values)
        max_value = max(filtered_values)
        print(max_value)
        if max_value > 0.5:
            card_id = y.index(max_value)
            print(card_id)
            card = CARDS_MAPPING[card_id]
            print(card)
            return card

    def decide_give_card(self):
        y = self.get_results()
        cards_values = y[12:24]
        cards_filter = self.get_cards_in_hand_filter()
        filtered_values = [value for i, value in enumerate(cards_values) if cards_filter[i]]
        max_value = max(filtered_values)
        if max_value > 0.5:
            card_id = y.index(max_value)
            card = CARDS_MAPPING[card_id]
            return card

    def decide_opponent(self):
        y = self.get_results()
        max_value = max(y[:4])
        opp_id = y.index(max_value)
        return self.correct_opponent_index(opp_id)

    def decide_exploding_kitten_placement(self):
        y = self.get_results()
        return y[-1]

    def decide_nope(self):
        y = self.get_results()
        return y[0] > 0.5

    def get_results(self):
        raise NotImplementedError


class RandomPlayer(Player):
    def get_results(self):
        return [random.random() for _ in range(30)]

    def choose_card(self):
        return random.choice(self.get_playable_cards())


class NeuralPlayer(Player):
    def get_results(self):
        return self.network.activate(self.adapter.input_array)

    # def choose_card(self):
    #     y = self.get_results()
    #     card_values = y[:10]
    #     return card_values.index(max(card_values))
