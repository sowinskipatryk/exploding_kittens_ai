from game_logic.players.base_player import BasePlayer
from game_logic.enums.card_names import CardName


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
        hand = self.hand.copy()
        del hand[CardName.DEFUSE]
        while True:
            print('Hand:')
            for i, k, v in enumerate(hand.items()):
                print(f'{i}) {k}: {len(v)}')
            answer = input('Which card do you want to play?')
            if answer.isdigit() and int(answer) in range(len(hand)):
                return int(answer)
            print('Invalid input. Please enter a valid card index.')

    def decide_give_card(self):
        while True:
            print('Hand:')
            for i, k, v in enumerate(self.hand.items()):
                print(f'{i}) {k}: {len(v)}')
            answer = input('Which card do you want to give opponent?')
            if answer.isdigit() and int(answer) in range(len(self.hand)):
                return int(answer)
            print('Invalid input. Please enter a valid card index.')

    def decide_opponent(self, game):
        opponents = [player is not self for player in game.players]
        while True:
            print('Opponents:')
            for i, opponent in enumerate(opponents):
                print(f'{i}) {opponent.name}')
            answer = input('Which opponent do you choose?')
            if answer.isdigit() and int(answer) in range(len(opponents)):
                return int(answer)
            print('Invalid input. Please enter a valid opponent index.')

    def decide_kitten_placement(self, game):
        while True:
            print(f'Cards in deck: {len(game.deck.cards)}')
            answer = input('Which position do you wish to place the Exploding Kitten in? ')
            if answer.isdigit() and int(answer) in range(len(game.deck.cards)):
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
