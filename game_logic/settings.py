class Settings:
    NUM_CARDS_DEALT = 7
    
    NUM_DEFUSE_CARDS = 6  # minimum 2 (game rules and implementation logic)
    NUM_SEE_THE_FUTURE_CARDS = 5
    NUM_NOPE_CARDS = 5
    NUM_SKIP_CARDS = 4
    NUM_SHUFFLE_CARDS = 4
    NUM_ATTACK_CARDS = 4
    NUM_FAVOR_CARDS = 4
    NUM_BEARD_CAT_CARDS = 4
    NUM_TACO_CAT_CARDS = 4
    NUM_HAIRY_POTATO_CAT_CARDS = 4
    NUM_CATTERMELON_CARDS = 4
    NUM_RAINBOW_RALPHING_CAT_CARDS = 4

    def __init__(self, num_players):
        self.num_players = num_players

        self.NUM_CARDS_IN_DECK = sum([self.NUM_DEFUSE_CARDS, self.NUM_SEE_THE_FUTURE_CARDS, self.NUM_NOPE_CARDS,
                                      self.NUM_SKIP_CARDS, self.NUM_SHUFFLE_CARDS, self.NUM_ATTACK_CARDS,
                                      self.NUM_FAVOR_CARDS, self.NUM_BEARD_CAT_CARDS, self.NUM_TACO_CAT_CARDS,
                                      self.NUM_HAIRY_POTATO_CAT_CARDS, self.NUM_CATTERMELON_CARDS,
                                      self.NUM_RAINBOW_RALPHING_CAT_CARDS, self.num_players - 1])
