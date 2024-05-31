class BaseCard:
    def __init__(self):
        self.name = self.__class__.__name__

    def __repr__(self):
        return self.name

    @property
    def is_exploding_kitten(self):
        return isinstance(self, Card.ExplodingKitten)

    @property
    def is_defuse(self):
        return isinstance(self, Card.Defuse)

    @property
    def is_attack(self):
        return isinstance(self, Card.Attack)

    @property
    def is_nope(self):
        return isinstance(self, Card.Nope)

    def use(self, game, **kwargs):
        raise NotImplementedError


class Card:
    class ExplodingKitten(BaseCard):
        def __init__(self):
            super().__init__()

        def use(self, game, **kwargs):
            player = game.players[game.current_player_index]
            defuse_card = player.get_defuse_card()
            if defuse_card:
                defuse_card.use(game, kitten_card=self)
            else:
                player.set_dead()

    class Defuse(BaseCard):
        def __init__(self):
            super().__init__()

        def use(self, game, **kwargs):
            player = game.players[game.current_player_index]
            player.hand.remove(self)
            idx = int(player.decide_exploding_kitten_placement() * len(game.deck))
            game.deck.insert_card(idx, kwargs.get('kitten_card'))

    class Attack(BaseCard):
        def __init__(self):
            super().__init__()

        def use(self, game, **kwargs):
            game.skip_draw = True
            game.current_player_index += 1
            game.turns_count = game.turns_count * 2

    class Skip(BaseCard):
        def __init__(self):
            super().__init__()

        def use(self, game, **kwargs):
            game.skip_draw = True

    class Favor(BaseCard):
        def __init__(self):
            super().__init__()

    class Shuffle(BaseCard):
        def __init__(self):
            super().__init__()

        def use(self, game, **kwargs):
            game.deck.shuffle()

    class SeeTheFuture(BaseCard):
        def __init__(self):
            super().__init__()

        def use(self, game, **kwargs):
            game.get_three_top_cards()

    class Nope(BaseCard):
        def __init__(self):
            super().__init__()

    class TacoCat(BaseCard):
        def __init__(self):
            super().__init__()

    class BeardCat(BaseCard):
        def __init__(self):
            super().__init__()

    class HairyPotatoCat(BaseCard):
        def __init__(self):
            super().__init__()

    class Cattermelon(BaseCard):
        def __init__(self):
            super().__init__()

    class RainbowRalphingCat(BaseCard):
        def __init__(self):
            super().__init__()
