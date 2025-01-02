import random
from collections import defaultdict

from game_logic.players import NeuralPlayer
from game_logic.deck import Deck
from game_logic.enums.card_names import CardName
from game_logic.settings import Settings

from log.config import logger


class Game:
    def __init__(self, players):
        self.num_players = len(players)

        if not 2 <= self.num_players <= 5:
            raise ValueError('This game requires 2-5 players to play!')

        self.players = players
        self.set_adapters()

        self.deck = Deck(self.num_players)
        self.settings = Settings(self.num_players)

        self.deal_defuse_cards()
        self.deck.shuffle()
        self.deal_deck_cards()
        self.deck.insert_exploding_kittens()
        self.deck.shuffle()

        self.current_player_id = random.randrange(len(self.players))
        self.turns_counter = 1
        self.extra_turns = 0
        self.skip_card_draw = False
        self.end_turn = False
        self.winner = None

    def set_adapters(self):
        neural_players = [player for player in self.players if isinstance(player, NeuralPlayer)]
        if not neural_players:
            return

        from network.adapter import NetworkAdapter
        adapter = NetworkAdapter(self)
        for player in neural_players:
            player.set_adapter(adapter)

    def get_current_player(self):
        return self.players[self.current_player_id]

    @property
    def num_alive_players(self):
        return sum([1 for player in self.players if player.is_alive])

    def deal_defuse_cards(self):
        for player in self.players:
            defuse_card = self.deck.get_initial_defuse_card()
            player.receive_card(defuse_card)

    def deal_deck_cards(self):
        for player in self.players:
            player.receive_cards([self.deck.draw_card() for _ in range(self.settings.NUM_CARDS_DEALT)])

    # def reset_deck_insight(self):
    #     for player in self.players:
    #         player.reset_deck_insight()

    def proceed_to_next_turn(self):
        if self.extra_turns > 0:
            self.extra_turns -= 1
        else:
            self.proceed_to_next_player()

        self.turns_counter += 1

    def proceed_to_next_player(self):
        self.current_player_id = (self.current_player_id + 1) % self.num_players

    def resolve_nopes(self):
        current_player_index = self.current_player_id
        nope_stack = []
        tries_since_nope = 0

        while tries_since_nope < self.num_players:
            tries_since_nope += 1
            current_player_index = (current_player_index + 1) % self.num_players
            current_player = self.players[current_player_index]

            if current_player.has_card(CardName.NOPE) and current_player.decide_nope():
                nope_card = current_player.play_card(CardName.NOPE)
                nope_card.action(self, current_player)
                nope_stack.append(current_player_index)
                tries_since_nope = 0

        if len(nope_stack) % 2 == 1:
            return True

    def play(self):
        logger.info("[Game] START")

        while self.num_alive_players > 1:
            logger.info(f"[Game] TURN {self.turns_counter}")  # !!!!! it should be called once for every turn but it does more often

            while True:
                curr_player = self.get_current_player()
                if curr_player.is_alive:
                    curr_player.turns_survived = self.turns_counter
                    break

                self.proceed_to_next_player()
                continue

            logger.debug(f"[Player] {curr_player.name} [status] alive")
            logger.debug(f"[Player] {curr_player.name} [extra turns] {self.extra_turns}")
            logger.debug(f"[Player] {curr_player.name} [hand] {curr_player.get_cards_count_dict()}")
            logger.debug(f"[Player] {curr_player.name} [deck insight] {curr_player.deck_insight}")

            num_tries = 0
            while curr_player.has_playable_cards() and curr_player.decide_play() and num_tries < 5:
                card_name = curr_player.choose_card()
                is_move_allowed = curr_player.has_enough_cards_to_play(card_name)
                if is_move_allowed:
                    card = curr_player.play_card(card_name)
                    # logger.info(f'[Player] {curr_player.name} [PLAY] {card}')
                    is_card_noped = self.resolve_nopes()
                    if is_card_noped:
                        logger.info(f'{curr_player.name} [USE] {card} noped')
                    else:
                        card.action(self, curr_player)
                        num_tries = 0
                num_tries += 1

            drawn_card = curr_player.draw_card(self.deck)

            if drawn_card == CardName.EXPLODING_KITTEN:
                drawn_card.action(self, curr_player)
            else:
                curr_player.receive_card(drawn_card)

            self.proceed_to_next_turn()

        self.winner = next(player for player in self.players if player.is_alive)
        logger.info(f"[Player] {self.winner.name} [WINNER]")
        logger.info("[Game] END")

        return self.game_stats()

    def game_stats(self):
        stats = defaultdict()
        stats['players'] = {}
        for player in self.players:
            stats['players'][player.name] = {
                'cards_played': player.cards_played,
                'cards_drawn': player.cards_drawn,
                'turns_survived': player.turns_survived,
                'interactions': {"attacks_received": player.attacks_received, "attacks_sent": player.attacks_sent}
            }

        stats['total_turns'] = self.turns_counter
        stats['winner'] = self.winner.name
        return stats
