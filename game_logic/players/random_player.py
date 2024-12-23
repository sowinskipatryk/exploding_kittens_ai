import random

from game_logic.players.base_player import BasePlayer


class RandomPlayer(BasePlayer):
    def decide_play(self):
        return random.choice([True, False])

    def decide_play_card(self):
        playable_cards_in_hand_mask = self.mask_playable_cards_in_hand()
        playable_cards_in_hand_indices = [i for i, v in enumerate(playable_cards_in_hand_mask) if v]
        return random.choice(playable_cards_in_hand_indices)

    def decide_give_card(self):
        cards_in_hand_mask = self.mask_cards_in_hand()
        cards_in_hand_indices = [i for i, v in enumerate(cards_in_hand_mask) if v]
        return random.choice(cards_in_hand_indices)

    def decide_opponent(self, game):
        opponents_indices_list = [idx for idx, player in enumerate(game.players) if player is not self]
        return random.choice(opponents_indices_list)

    def decide_kitten_placement(self, game):
        return random.randrange(0, max(1, len(game.deck)))

    def decide_nope(self):
        return random.choice([True, False])
