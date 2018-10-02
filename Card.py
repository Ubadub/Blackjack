from enum import Enum

Rank = Enum('Rank', 'ACE TWO THREE FOUR FIVE SIX SEVEN EIGHT NINE TEN JACK QUEEN KING')

class Suit(Enum):
    SPADES = "Spades"
    HEARTS = "Hearts"
    DIAMONDS = "Diamonds"
    CLUBS = "Clubs"

    def __repr__(self):
        return self.name

class Card():
    """ Represents a card in a deck of cards. """
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        if self.rank is Rank.ACE:
            rank_name = 'Ace'
        elif self.rank is Rank.JACK:
            rank_name = 'Jack'
        elif self.rank is Rank.QUEEN:
            rank_name = 'Queen'
        elif self.rank is Rank.KING:
            rank_name = 'King'
        else:
            rank_name = self.rank.value
        return '{} of {}'.format(rank_name, self.suit.value)