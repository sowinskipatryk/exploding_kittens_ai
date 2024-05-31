class NetworkAdapter:
    CARDS_IN_HAND_TYPES = 0
    DEFUSE_CARDS_NUM = 80
    CARDS_IN_OPPONENTS_HANDS_NUM = 5
    TOP_DECK_CARDS = 75
    DECK_SIZE = 85
    LAST_PLAYED_CARD = 90
    ALIVE_PLAYERS = 95
    ALIVE_PLAYERS_NUM = 100

    def __init__(self, players_num):
        self.players_num = players_num
        self.input_array = [0 for _ in range(100)]

        input_array = [
            # Player's Hand (binary vector for each card type)
            1, 0, 1, 0, 0, 1, 0, 0,  # Example: [Defuse, Attack, Shuffle]

            # Player's Defuse Count (normalized)
            0.5,  # Example: 1 Defuse card, normalized (assuming max possible is 2)

            # Top Deck Cards (binary vector for known top cards)
            0, 0, 0, 0, 0, 1, 1, 0,  # Example: [Shuffle, See the Future] are known top cards

            # Deck Size (normalized)
            0.3,  # Example: 15 cards left in the deck, normalized (assuming starting size of 50)

            # Player Pending Turns (normalized)
            0.0,  # Example: no extra turns pending

            # Opponent Pending Turns (normalized)
            0.5, 0.0, 0.0,  # Example: first opponent has an extra turn

            # Last Played Card (binary vector for each card type)
            0, 0, 0, 0, 1, 0, 0, 0,  # Example: last played card was Favor

            # Player's Status
            1,  # Player is alive

            # Opponent's Statuses
            1, 1, 1,  # All opponents are alive

            # Number of Players (normalized)
            0.75,  # Example: 4 players still in the game (assuming a max of 5)
        ]

    def set_player_cards(self):
        pass

    def set_alive_players_count(self, game):
        return self.normalize_alive_players_count(game.alive_players_count)

    def set_defuse_cards_count(self, player):
        return self.normalize_defuse_cards_count(player.defuse_cards_count)

    def set_deck_count(self, game):
        return self.normalize_deck_count(len(game.deck))

    def normalize_alive_players_count(self, count):
        return count / 5

    def normalize_defuse_cards_count(self, count):
        return count / 6

    def normalize_deck_count(self, count):
        return count / 56

# play:
# skip
# attack
# favor
# shuffle
# seethefuture
# nope
#
