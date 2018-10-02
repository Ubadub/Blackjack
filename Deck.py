import random

from Card import *

class Deck():
    """ Represents one or more Decks. Contains 52 * num_decks cards """
    def __init__(self, num_decks=1):
        self.num_decks = num_decks
        self.cards = num_decks * [Card(rank, suit) for rank in Rank for suit in Suit]
        self.shuffle()

    # Instance Methods

    def add(self, cards):
        self.cards.extend(cards)

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self, num=1):
        l = []
        for i in range(num):
            l.append(self.cards.pop())
        return l