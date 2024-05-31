class BaseCard:
    def __init__(self):
        self.name = self.__class__.__name__
        self.is_playable = True

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
    def is_skip(self):
        return isinstance(self, Card.Skip)

    @property
    def is_nope(self):
        return isinstance(self, Card.Nope)

    def action(self, game, **kwargs):
        pass


class Card:
    class ExplodingKitten(BaseCard):
        def __init__(self):
            super().__init__()
            self.is_playable = False

        def action(self, game, **kwargs):
            player = game.players[game.current_player_index]
            defuse_card = player.get_defuse_card()
            if defuse_card:
                defuse_card.action(game, kitten_card=self)
            else:
                player.set_dead()

    class Defuse(BaseCard):
        def __init__(self):
            super().__init__()
            self.is_playable = False

        def action(self, game, **kwargs):
            player = game.players[game.current_player_index]
            player.hand.remove(self)
            idx = int(player.decide_exploding_kitten_placement() * len(game.deck))
            game.deck.insert_card(idx, kwargs.get('kitten_card'))

    class Attack(BaseCard):
        def __init__(self):
            super().__init__()

        def action(self, game, **kwargs):
            game.end_turn = True
            game.next_player()
            if game.turns_count < 2:
                game.turns_count = 2
            else:
                game.turns_count += 2

    class Skip(BaseCard):
        def __init__(self):
            super().__init__()

        def action(self, game, **kwargs):
            game.end_turn = True
            game.turns_count -= 1

    class Favor(BaseCard):
        def __init__(self):
            super().__init__()

    class Shuffle(BaseCard):
        def __init__(self):
            super().__init__()

        def action(self, game, **kwargs):
            game.deck.shuffle()

    class SeeTheFuture(BaseCard):
        def __init__(self):
            super().__init__()

        def action(self, game, **kwargs):
            game.deck.get_top_three_cards()

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
