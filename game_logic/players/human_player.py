from game_logic.players.base_player import BasePlayer
from game_logic.cards import PLAYABLE_CARD_NAMES, HAND_CARD_NAMES


class HumanPlayer(BasePlayer):
    def decide_play(self):
        while True:
            answer = input('Do you want to play some cards? (y/n): ')
            if answer == 'y':
                return True
            elif answer == 'n':
                return False
            else:
                print('Invalid input. Please enter y or n.')

    def decide_play_card(self):
        while True:
            print('Hand:')
            for i, playable_card in enumerate(PLAYABLE_CARD_NAMES):
                print(f"{i}) {playable_card}: {len(self.hand[playable_card])}")
            answer = input(f'Which card do you want to play? (0-{len(PLAYABLE_CARD_NAMES) - 1}): ')
            if answer.isdigit() and int(answer) in range(len(PLAYABLE_CARD_NAMES)):
                chosen_card_name = PLAYABLE_CARD_NAMES[int(answer)]
                return HAND_CARD_NAMES.index(chosen_card_name)
            print('Invalid input. Please enter a valid card index.')

    def decide_give_card(self):
        while True:
            print('Hand:')
            for i, (k, v) in enumerate(self.hand.items()):
                print(f'{i}) {k}: {len(v)}')
            answer = input(f'Which card do you want to give opponent? (0-{len(self.hand)}): ')
            if answer.isdigit() and int(answer) in range(len(self.hand)):
                return int(answer)
            print('Invalid input. Please enter a valid card index.')

    def decide_opponent(self, game):
        opponents = [player for player in game.players if player is not self]
        while True:
            print('Opponents:')
            for i, opponent in enumerate(opponents):
                print(f'{i}) {opponent.name}')
            answer = input('Which opponent do you choose? ')
            if answer.isdigit() and int(answer) in range(len(opponents)):
                chosen_opponent = opponents[int(answer)]
                return game.players.index(chosen_opponent)
            print('Invalid input. Please enter a valid opponent index.')

    def decide_kitten_placement(self, game):
        cards_in_deck = len(game.deck)
        while True:
            print(f'Cards in deck: {cards_in_deck}')
            answer = input(f'Which position do you wish to place the Exploding Kitten in? (0-{cards_in_deck - 1}): ')
            if answer.isdigit() and int(answer) in range(len(game.deck)):
                return int(answer)
            else:
                print('Invalid input. Please enter a valid deck index.')

    def decide_nope(self):
        while True:
            answer = input('Do you want to play the Nope card? (y/n): ')
            if answer == 'y':
                return True
            elif answer == 'n':
                return False
            else:
                print('Invalid input. Please enter y or n.')
