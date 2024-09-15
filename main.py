from game_logic.enums.player_types import PlayerType
from game_logic.players.human_player import HumanPlayer
from game_logic.players.neural_player import NeuralPlayer
from game_logic.players.random_player import RandomPlayer


def main_loop():
    print("Menu:")
    print("1. Play the game")
    print("2. Teach neural network to play the game")

    while True:
        choice = input("Enter your choice: ")

        if choice == '1':
            while True:
                print('Enter player types (Random, Human, Neural) separated by commas for each of the (2-5) players')
                player_types_input = input().split(',')
                try:
                    player_types = [PlayerType[ptype.strip().upper()] for ptype in player_types_input]
                except (ValueError, KeyError):
                    print('Each player must be of type Random, Human or Neural!')
                    continue

                if not 2 <= len(player_types) <= 5:
                    print('This game is crafted for 2-5 players!')
                    continue

                break

            from game_logic.game import Game
            players = setup_players(player_types)
            game = Game(players)
            game.play()
            break

        elif choice == '2':
            while True:
                players_num = input('How many players do you want to train on (2-5): ')
                if players_num.isdigit() and 2 <= int(players_num) <= 5:
                    break
                else:
                    print('Invalid players number:', players_num)

            from network.manager import teach_network
            teach_network(players_num=5)
            break
        else:
            print("Invalid choice! Please enter a valid option [1-2]")

def setup_players(player_types):
    players = []
    for idx, p_type in enumerate(player_types):
        if p_type == PlayerType.HUMAN:
            players.append(HumanPlayer(idx))
        elif p_type == PlayerType.NEURAL:
            players.append(NeuralPlayer(idx, network=None, adapter=None))
        elif p_type == PlayerType.RANDOM:
            players.append(RandomPlayer(idx))
    return players


if __name__ == "__main__":
    main_loop()
