class BaseCard:
    def __init__(self):
        self.name = self.__class__.__name__

    def __repr__(self):
        return self.name

    @property
    def is_exploding_kitten(self):
        return isinstance(self, Card.ExplodingKitten)

    def is_defuse(self):
        return isinstance(self, Card.Defuse)

    def use(self, game, **kwargs):
        raise NotImplementedError


class Card:
    class ExplodingKitten(BaseCard):
        def __init__(self):
            super().__init__()

        def use(self, game, **kwargs):
            player = game.players[game.turn_index]
            defuse_card = player.get_defuse_card()
            if defuse_card:
                defuse_card.use(game, kitten_card=self)
            else:
                player.set_dead()

    class Defuse(BaseCard):
        def __init__(self):
            super().__init__()

        def use(self, game, **kwargs):
            player = game.players[game.turn_index]
            player.hand.pop(self)
            idx = player.decide_exploding_kitten_placement()
            game.deck.put_card(idx, kwargs.get('kitten_card'))

    class Attack(BaseCard):
        def __init__(self):
            super().__init__()

    class Skip(BaseCard):
        def __init__(self):
            super().__init__()

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
