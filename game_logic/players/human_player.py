from game_logic.players.base_player import BasePlayer


class HumanPlayer(BasePlayer):
    def get_results(self):
        return self.network.activate(self.adapter.input_array)
