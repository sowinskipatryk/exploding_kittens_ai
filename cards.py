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


class Card:
    class ExplodingKitten(BaseCard):
        def __init__(self):
            super().__init__()

    class Defuse(BaseCard):
        def __init__(self):
            super().__init__()

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

    class SeeTheFuture(BaseCard):
        def __init__(self):
            super().__init__()

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
