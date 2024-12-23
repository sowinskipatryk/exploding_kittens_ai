from game_logic.players.human_player import HumanPlayer
from game_logic.players.neural_player import NeuralPlayer
from game_logic.players.random_player import RandomPlayer


def player_factory(player_info):
    player_type = player_info.get('type')
    player_name = player_info.get('name')

    if not player_type or not player_name:
        raise ValueError("Player info must contain 'type' and 'name'.")

    if player_type == 'Random':
        return RandomPlayer(player_name)
    elif player_type == 'Neural':
        network_file = player_info.get('network_file')
        if not network_file:
            raise ValueError(f"Missing 'network_file' for NeuralPlayer {player_name}")
        from network.manager import load_network
        network = load_network(network_file)
        return NeuralPlayer(player_name, network=network)
    elif player_type == 'Human':
        return HumanPlayer(player_name)
    else:
        raise ValueError(f"Unsupported player type: {player_type}")
