from abc import ABC, abstractmethod

from log.config import logger
from game_logic.enums.card_names import CardName


class BaseCard(ABC):
    is_pair = False
    is_playable = True
    is_hand_card = True

    @property
    @abstractmethod
    def name(self):
        pass

    def __repr__(self):
        return self.name.value

    def __eq__(self, other):
        return self.name == other

    def action(self, game, player, **kwargs):
        logger.info(f"[Card] {player.name} [ACTION] {self}")
        self._action_logic(game, player, **kwargs)

    @abstractmethod
    def _action_logic(self, game, player, **kwargs):
        pass


class ExplodingKitten(BaseCard):
    name = CardName.EXPLODING_KITTEN
    is_playable = False
    is_hand_card = False

    def _action_logic(self, game, player, **kwargs):
        has_defuse_card = player.has_card(CardName.DEFUSE)
        if has_defuse_card:
            card = player.play_card(CardName.DEFUSE)
            card.action(game, player, exploding_kitten_card=self)
        else:
            player.explode()
            logger.debug(f"[Player] {player.name} [EXPLODE]")


class Defuse(BaseCard):
    name = CardName.DEFUSE
    is_playable = False

    def _action_logic(self, game, player, **kwargs):
        exploding_kitten_card = kwargs.get('exploding_kitten_card')
        kitten_placement_index = player.decide_kitten_placement(game)
        game.deck.insert_card(kitten_placement_index, exploding_kitten_card)
        if not player.used_defuse:
            player.used_defuse = True


class Attack(BaseCard):
    name = CardName.ATTACK

    def _action_logic(self, game, player, **kwargs):
        if not game.extra_turns:
            game.extra_turns += 1
        else:
            game.extra_turns += 2

        game.proceed_to_next_player()
        game.turns_counter += 1


class Skip(BaseCard):
    name = CardName.SKIP

    def _action_logic(self, game, player, **kwargs):
        if game.extra_turns > 0:
            game.extra_turns -= 1
        else:
            game.proceed_to_next_player()


class Favor(BaseCard):
    name = CardName.FAVOR

    def _action_logic(self, game, player, **kwargs):
        opponent = player.choose_opponent(game)
        if not opponent:
            return
        card = opponent.give_card()
        player.receive_card(card)


class Shuffle(BaseCard):
    name = CardName.SHUFFLE

    def _action_logic(self, game, player, **kwargs):
        game.deck.shuffle()


class SeeTheFuture(BaseCard):
    name = CardName.SEE_THE_FUTURE

    def _action_logic(self, game, player, **kwargs):
        game.deck.check_three_top_cards()


class Nope(BaseCard):
    name = CardName.NOPE

    def _action_logic(self, game, player, **kwargs):
        pass  # logic implemented in resolve_nopes()


class PairCard(BaseCard, ABC):
    is_pair = True
        
    def _action_logic(self, game, player, **kwargs):
        opponent_id = player.decide_opponent(game)
        opponent = game.players[opponent_id]
        player.steal_card(opponent)


class TacoCat(PairCard):
    name = CardName.TACO_CAT


class BeardCat(PairCard):
    name = CardName.BEARD_CAT


class HairyPotatoCat(PairCard):
    name = CardName.HAIRY_POTATO_CAT


class Cattermelon(PairCard):
    name = CardName.CATTERMELON


class RainbowRalphingCat(PairCard):
    name = CardName.RAINBOW_RALPHING_CAT


CARDS_CLASSES_LIST = [ExplodingKitten, Defuse, Attack, Skip, Favor, Shuffle, SeeTheFuture, Nope, TacoCat, BeardCat,
                      HairyPotatoCat, Cattermelon, RainbowRalphingCat]

PAIR_CARD_NAMES = [card.name for card in CARDS_CLASSES_LIST if card.is_pair]
PLAYABLE_CARD_NAMES = [card.name for card in CARDS_CLASSES_LIST if card.is_playable]
HAND_CARD_NAMES = [card.name for card in CARDS_CLASSES_LIST if card.is_hand_card]
