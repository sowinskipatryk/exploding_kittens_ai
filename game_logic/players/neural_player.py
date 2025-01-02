import math

from game_logic.cards import PLAYABLE_CARD_NAMES, HAND_CARD_NAMES
from game_logic.players.base_player import BasePlayer
from log.config import logger


PLAY_DECISION_INDEX = 0
NOPE_DECISION_INDEX = 1
KITTEN_PLACEMENT_DECISION_INDEX = 2
PLAY_CARD_DECISION_INDEX = 3
GIVE_CARD_DECISION_INDEX = PLAY_CARD_DECISION_INDEX + len(PLAYABLE_CARD_NAMES)
OPPONENT_DECISION_INDEX = GIVE_CARD_DECISION_INDEX + len(HAND_CARD_NAMES)


class NeuralPlayer(BasePlayer):
    def __init__(self, name, network=None):
        super().__init__(name)
        self.network = network
        self.adapter = None

    def set_adapter(self, adapter):
        self.adapter = adapter

    def set_network(self, network):
        self.network = network

    def get_player_state(self):
        hand = self.get_cards_count_list()
        pair_card_playable = [1 if self.has_playable_pair_cards() else 0]
        return hand + pair_card_playable

    def get_scores(self):
        game_state = self.adapter.get_game_state()
        player_state = self.get_player_state()
        inputs = game_state + player_state
        return self.network.activate(inputs)

    @staticmethod
    def is_above_threshold(value, threshold=0.5):
        return value > threshold

    @staticmethod
    def mask_invalid_choices(scores, mapping):
        return [score if mapping[i] else 0.0 for i, score in enumerate(scores)]

    def mask_opponents(self, game):
        return [1 if player is not self else 0 for player in game.players]

    @staticmethod
    def log_return_value(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            logger.debug(f"[NPlayer] {func.__name__} returned: {result}")
            return result
        return wrapper

    @log_return_value
    def decide_nope(self):
        scores = self.get_scores()
        nope_score = scores[NOPE_DECISION_INDEX]
        output = self.is_above_threshold(nope_score)
        return output

    @log_return_value
    def decide_play(self):
        scores = self.get_scores()
        play_score = scores[PLAY_DECISION_INDEX]
        output = self.is_above_threshold(play_score)
        return output

    @log_return_value
    def decide_kitten_placement(self, game):
        scores = self.get_scores()
        kitten_placement_score = scores[KITTEN_PLACEMENT_DECISION_INDEX]
        output = math.floor(kitten_placement_score * len(game.deck))
        return output

    @log_return_value
    def decide_play_card(self):
        scores = self.get_scores()
        cards_scores = scores[PLAY_CARD_DECISION_INDEX:GIVE_CARD_DECISION_INDEX]
        playable_cards_in_hand_mask = self.mask_playable_cards_in_hand()
        masked_scores = self.mask_invalid_choices(cards_scores, playable_cards_in_hand_mask)
        max_score = max(masked_scores)
        output = masked_scores.index(max_score)
        return output

    @log_return_value
    def decide_give_card(self):
        scores = self.get_scores()
        cards_scores = scores[GIVE_CARD_DECISION_INDEX:OPPONENT_DECISION_INDEX]
        cards_in_hand_mask = self.mask_cards_in_hand()
        masked_scores = self.mask_invalid_choices(cards_scores, cards_in_hand_mask)
        max_score = max(masked_scores)
        output = masked_scores.index(max_score)
        return output

    @log_return_value
    def decide_opponent(self, game):
        scores = self.get_scores()
        players_scores = scores[OPPONENT_DECISION_INDEX:]
        opponents_mask = self.mask_opponents(game)
        masked_scores = self.mask_invalid_choices(players_scores, opponents_mask)
        max_score = max(masked_scores)
        output = masked_scores.index(max_score)
        return output
