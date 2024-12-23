import random

from game_logic.cards import (Defuse, SeeTheFuture, Nope, Skip, Shuffle, Attack, Favor, BeardCat, TacoCat,
                              HairyPotatoCat, Cattermelon, RainbowRalphingCat, ExplodingKitten)
from log.config import logger
from game_logic.settings import Settings


class Deck:
    def __init__(self, players_num):
        self._players_num = players_num
        self.cards = self._create_deck()

    def _create_deck(self):
        deck = []

        # Single cards
        deck += [Defuse() for _ in range(min(2, Settings.NUM_DEFUSE_CARDS - self._players_num))]
        deck += [SeeTheFuture() for _ in range(Settings.NUM_SEE_THE_FUTURE_CARDS)]
        deck += [Nope() for _ in range(Settings.NUM_NOPE_CARDS)]
        deck += [Skip() for _ in range(Settings.NUM_SKIP_CARDS)]
        deck += [Shuffle() for _ in range(Settings.NUM_SHUFFLE_CARDS)]
        deck += [Attack() for _ in range(Settings.NUM_ATTACK_CARDS)]
        deck += [Favor() for _ in range(Settings.NUM_FAVOR_CARDS)]

        # Pair cards
        deck += [BeardCat() for _ in range(Settings.NUM_BEARD_CAT_CARDS)]
        deck += [TacoCat() for _ in range(Settings.NUM_TACO_CAT_CARDS)]
        deck += [HairyPotatoCat() for _ in range(Settings.NUM_HAIRY_POTATO_CAT_CARDS)]
        deck += [Cattermelon() for _ in range(Settings.NUM_CATTERMELON_CARDS)]
        deck += [RainbowRalphingCat() for _ in range(Settings.NUM_RAINBOW_RALPHING_CAT_CARDS)]

        return deck

    def shuffle(self):
        logger.debug(f"[Deck] State before shuffling cards ({len(self)}): {self.cards}")
        random.shuffle(self.cards)
        logger.debug(f"[Deck] State after shuffling cards ({len(self)}): {self.cards}")

    def draw_card(self):
        logger.debug(f"[Deck] State before drawing ({len(self)}): {self.cards}")
        assert len(self) > 0  # should never happen since the last card in deck will always be the Exploding Kitten that ends the game
        card = self.cards.pop()
        logger.debug(f"[Deck] Drawn card: {card}")
        logger.debug(f"[Deck] State after drawing ({len(self)}): {self.cards}")
        return card

    def insert_card(self, pos, card):
        logger.debug(f"[Deck] State before insertion ({len(self)}): {self.cards}")
        self.cards.insert(pos, card)
        logger.debug(f"[Deck] Inserting card {card} at index {pos}")
        logger.debug(f"[Deck] State after insertion ({len(self)}): {self.cards}")

    def check_three_top_cards(self):
        top_cards = self.cards[:-4:-1]
        return top_cards

    def __len__(self):
        return len(self.cards)

    @staticmethod
    def get_initial_defuse_card():
        return Defuse()

    def insert_exploding_kittens(self):
        logger.debug(f"[Deck] State before insertion ({len(self)}): {self.cards}")
        self.cards.extend([ExplodingKitten() for _ in range(self._players_num - 1)])
        logger.debug(f"[Deck] State after insertion ({len(self)}): {self.cards}")

    def insert_remaining_defuse_cards(self):
        logger.debug(f"[Deck] State before insertion ({len(self)}): {self.cards}")
        self.cards.extend([Defuse() for _ in range(min(2, 6 - self._players_num))])
        logger.debug(f"[Deck] State after insertion ({len(self)}): {self.cards}")
