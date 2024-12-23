from game_logic.game import Game
from game_logic.players import player_factory


def main():
    players_configs = [
        {'type': 'Human', 'name': 'R1'},
        {'type': 'Neural', 'name': 'N2', 'network_file': 'best_genome5.pkl'},
        {'type': 'Random', 'name': 'R3'},
        {'type': 'Random', 'name': 'R4'},
        {'type': 'Random', 'name': 'R5'}
    ]

    players = [player_factory(config) for config in players_configs]

    game = Game(players)
    game.play()


if __name__ == "__main__":
    main()
