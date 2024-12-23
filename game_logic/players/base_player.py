import random
from abc import ABC, abstractmethod
from collections import defaultdict

from game_logic.cards import PLAYABLE_CARD_NAMES, HAND_CARD_NAMES, PAIR_CARD_NAMES
from log.config import logger


class BasePlayer(ABC):
    is_neural = False

    def __init__(self, name):
        self.name = name
        self.hand = {card: [] for card in HAND_CARD_NAMES}
        self.deck_insight = []
        self.is_alive = True
        self.used_defuse = False

        self.cards_played = defaultdict(int)
        self.cards_drawn = 0
        self.turns_survived = 0
        self.attacks_sent = 0
        self.attacks_received = 0

    def count_all_cards(self):
        return sum(len(cards) for cards in self.hand.values())

    def has_cards(self):
        return self.count_all_cards() > 0

    def has_playable_pair_cards(self):
        pair_cards = self.get_pair_cards()
        pair_cards_count = [len(value) for key, value in self.hand.items() if key in pair_cards]
        return any(count >= 2 for count in pair_cards_count)

    def has_card(self, card_name):
        return len(self.hand[card_name]) > 0

    def get_cards_num(self, card_name):
        return len(self.hand[card_name])

    def remove_from_hand(self, card_name):
        return self.hand[card_name].pop()

    def get_cards_count_dict(self):
        return {card.value: len(instances) for card, instances in self.hand.items()}

    def get_cards_count_list(self):
        return [len(value) for value in self.hand.values()]

    def mask_cards_in_hand(self):
        return [1 if self.hand[card] else 0 for card in self.hand]

    def mask_playable_cards_in_hand(self):
        return [1 if self.hand[card] else 0 for card in PLAYABLE_CARD_NAMES]

    def has_playable_cards(self):
        return any(self.hand[card] for card in PLAYABLE_CARD_NAMES)

    def receive_card(self, card):
        self.hand[card.name].append(card)
        logger.debug(f'[Player] {self.name} [RECEIVE] {card}')
        logger.debug(f"[Player] {self.name} [hand] {self.get_cards_count_dict()}")

    def receive_cards(self, cards):
        for card in cards:
            self.receive_card(card)

    def explode(self):
        self.is_alive = False

    def draw_card(self, deck):
        card = deck.draw_card()
        self.cards_drawn += 1
        logger.info(f"[Player] {self.name} [DRAW] {card}")
        return card

    def get_pair_cards(self):
        return [card for card in self.hand if card.name in PAIR_CARD_NAMES]

    def check_pair_card(self, card_name):
        card = self.get_card_by_name(card_name)
        return card.is_pair

    def play_card(self, card_name):
        is_pair_card = self.check_pair_card(card_name)
        num_cards = 2 if is_pair_card else 1
        for i in range(num_cards):
            card = self.remove_from_hand(card_name)
        self.cards_played[card_name.value] += 1
        logger.info(f"[Player] {self.name} [PLAY] {card}")
        logger.debug(f"[Player] {self.name} [hand] {self.get_cards_count_dict()}")
        return card

    def has_enough_cards_to_play(self, card_name):
        if self.hand[card_name]:
            if self.hand[card_name][0].is_pair:
                return len(self.hand[card_name]) >= 2
            return len(self.hand[card_name]) >= 1

    def get_card_by_name(self, card_name):
        if self.hand[card_name]:
            return self.hand[card_name][0]

    def steal_card(self, opponent):
        if not opponent.has_cards():
            return
        card_names_got = [card_name for card_name in opponent.hand if opponent.has_card(card_name)]
        card_name = random.choice(card_names_got)
        card = opponent.remove_from_hand(card_name)
        logger.info(f'[Player] {self.name} [STEAL] {card}')
        self.receive_card(card)
        self.attacks_sent += 1

    #
    # def reset_deck_insight(self):
    #     self.deck_insight = []

    def give_card(self):
        card_id = self.decide_give_card()
        card_names_list = list(self.hand.keys())
        card_name = card_names_list[card_id]
        assert self.hand[card_name]
        self.attacks_received += 1
        logger.info(f'[Player] {self.name} [GIVE] {card_name.value}')
        return self.hand[card_name].pop()

    def choose_card(self):
        card_id = self.decide_play_card()
        card = PLAYABLE_CARD_NAMES[card_id]
        logger.info(f'[Player] {self.name} [CHOOSE] {card.value}')
        return card

    def choose_opponent(self, game):
        opponent_id = self.decide_opponent(game)
        opponent = game.players[opponent_id]
        if opponent.is_alive and opponent.has_cards():
            return opponent

    @abstractmethod
    def decide_play(self):
        pass

    @abstractmethod
    def decide_play_card(self):
        pass

    @abstractmethod
    def decide_give_card(self):
        pass

    @abstractmethod
    def decide_kitten_placement(self, game):
        pass

    @abstractmethod
    def decide_nope(self):
        pass

    @abstractmethod
    def decide_opponent(self, game):
        pass
