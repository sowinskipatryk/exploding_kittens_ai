import random

from game_logic.players.base_player import BasePlayer


class RandomPlayer(BasePlayer):
    def decide_play(self):
        return random.choice([True, False])

    def decide_play_card(self):
        return random.randrange(len(self.hand) - 1)  # exclude defuse card

    def decide_give_card(self):
        return random.randrange(len(self.hand))

    def decide_opponent(self, game):
        return random.randrange(game.players_num)

    def decide_kitten_placement(self, game):
        return random.random()

    def decide_nope(self):
        return random.choice([True, False])
