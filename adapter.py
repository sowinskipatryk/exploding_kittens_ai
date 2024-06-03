"""
INPUT:
12 CARD TYPES COUNT (Defuse, Attack, Skip, Nope, SeeTheFuture, Favor, Shuffle, BeardCat, HairyPotatoCat, Cattermelon, TacoCat, RainbowRalphingCat)
# 39 ONE-HOT TOP THREE CARDS (ExplodingKitten, Defuse, Attack, Skip, Nope, SeeTheFuture, Favor, Shuffle, BeardCat, HairyPotatoCat, Cattermelon, TacoCat, RainbowRalphingCat)
4 OPPONENTS CARDS COUNT
1 PLAYER DEFUSE CARDS COUNT
1 DECK SIZE
5 PLAYERS STATUSES
1 TURNS LEFT
5 ONE-HOT TURN

OUTPUT:
1 DON'T PLAY THE CARD
11 PLAY CARD TYPE (Attack, Skip, Nope, SeeTheFuture, Favor, Shuffle, BeardCat, HairyPotatoCat, Cattermelon, TacoCat, RainbowRalphingCat)
4 CHOOSE OPPONENT
1 PLACE EXPLODING KITTEN IN DECK
"""


class NetworkAdapter:
    CARD_TYPES_COUNT = 0
    OPPONENTS_CARDS_COUNT = 12
    DEFUSE_CARDS_COUNT = 16
    DECK_SIZE = 17
    PLAYERS_STATUSES = 18
    TURNS_LEFT = 23
    TURN = 24

    def __init__(self, players_num):
        self.players_num = players_num
        self.input_array = [0 for _ in range(29)]

        self.set_all_players_alive()

    def set_all_players_alive(self):
        for i in range(self.players_num):
            self.set_player_alive(i)

    def set_player_alive(self, index):
        self.input_array[self.PLAYERS_STATUSES + index] = 1.

    def set_player_dead(self, index):
        self.input_array[self.PLAYERS_STATUSES + index] = 0.

    def set_player_cards(self):
        pass

    def set_defuse_cards_count(self, player):
        self.input_array[self.DEFUSE_CARDS_COUNT] = self.normalize_defuse_cards_count(player.defuse_cards_count)

    def set_deck_size(self, game):
        self.input_array[self.DECK_SIZE] = self.normalize_deck_size(len(game.deck))

    @staticmethod
    def normalize_defuse_cards_count(count):
        return count / 6

    @staticmethod
    def normalize_deck_size(count):
        return count / 56
