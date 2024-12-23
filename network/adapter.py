class NetworkAdapter:
    def __init__(self, game):
        self.game = game

    def get_game_state(self):
        extra_turns = self.get_extra_turns()
        players_cards_count = self.get_players_cards_count()
        players_used_defuse = self.get_players_used_defuse()
        players_status = self.get_players_status()
        deck_size = self.get_deck_size()
        return extra_turns + players_cards_count + players_used_defuse + players_status + deck_size

    def get_extra_turns(self):
        return [self.game.extra_turns]

    def get_players_cards_count(self):
        return [player.count_all_cards() for player in self.game.players]

    def get_players_used_defuse(self):
        return [1 if player.used_defuse else 0 for player in self.game.players]

    def get_players_status(self):
        return [1 if player.is_alive else 0 for player in self.game.players]

    def get_deck_size(self):
        return [len(self.game.deck)]

    def normalize_deck_size(self, count):
        return count / self.game.settings.NUM_CARDS_IN_DECK
