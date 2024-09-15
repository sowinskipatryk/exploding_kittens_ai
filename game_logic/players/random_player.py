import random

from game_logic.players.base_player import BasePlayer


class RandomPlayer(BasePlayer):
    def get_results(self):
        return [random.random() for _ in range(30)]

    def choose_card(self):
        return random.choice(self.get_playable_cards())
