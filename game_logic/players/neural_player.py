from game_logic.players.base_player import BasePlayer


class NeuralPlayer(BasePlayer):
    def __init__(self, index, network, adapter):
        super().__init__(index)
        self.network = network
        self.adapter = adapter

    def get_results(self):
        return self.network.activate(self.adapter.input_array)

    # def choose_card(self):
    #     y = self.get_results()
    #     card_values = y[:10]
    #     return card_values.index(max(card_values))
