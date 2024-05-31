from game import Game


def main_loop():
    game = Game(players_count=5)
    game.play()

    # print("Menu:")
    # print("1. Teach neural network to play the game")
    # print("2. Play against taught AI")
    #
    # while True:
    #     choice = input("Enter your choice: ")
    #
    #     if choice == '1':
    #         # train_neural_network()
    #         break
    #     elif choice == '2':
    #         # play_game_with_ai()
    #         game = Game(players_num=5)
    #         game.play()
    #         break
    #     else:
    #         print("Invalid choice! Please enter a valid option (1-2)")


if __name__ == "__main__":
    main_loop()
