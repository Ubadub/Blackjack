from itertools import chain

from Card import *

class BasePlayer():
    """docstring for Base Player"""
    def __init__(self):
        self._hands = []

    # Properties

    @property
    def hands(self):
        return self._hands

    @property
    def num_hands(self):
        return len(self._hands)

    # Setters
    @hands.setter
    def hands(self, h):
        self._hands = h

    def add_hand(self, h):
        self._hands.append(h)

    # Instance methods

    def deal(self, cards, idx_hand=0):
        """Deals the given cards to the given hand."""
        while self.num_hands < idx_hand + 1:
            self.add_hand([])
            
        self.hands[idx_hand].extend(cards)

    def get_hand(self, i = 0):
        return self.hands[i]

    def print_hand(self, idx_hand=0):
        """Print a single hand."""
        hand = self.hands[idx_hand]
        for card in hand:
            print('   ', card)
        print('Total:', self.score(idx_hand), '\n')

    def print_all_hands(self):
        n = self.num_hands
        if n > 1:
            print("You are currently playing {} hand(s):".format(self.num_hands))
        
        for i in range(self.num_hands):
            self.print_hand(i)
    
    def reset(self):
        """
        Resets BasePlayer for playing in another round (NOT another game).
        Empties hands and returns those cards for recycling.
        Resets bet to 0.
        """
        l = self.hands
        self.hands = []
        return l

    def score(self, idx_hand=0):
        hand = self.hands[idx_hand]
        
        score = 0
        aces = 0
        for card in hand:
            if card.rank is Rank.ACE:
                aces += 1
            else:
                score += min(card.rank.value, 10)

        if score > 10: # score too high for aces to count as 11
            score += aces
        elif aces >= 1: # multiple aces, score low enough to count one as 11
            if aces <= 11 - score:
                score += 11
                aces -= 1
            score += aces
        return score

class Dealer(BasePlayer):
    """Represents the Blackjack Dealer (plays for the House)."""

    UPCARD_INDEX = 0 # index of the upcard in a Dealer's hand
    HOLE_INDEX   = 1 # index of the hole card in a Dealer's hand

    def __init__(self):
        super(Dealer, self).__init__()
        self._is_hole_visible = False

    # Properties

    @property
    def is_hole_visible(self):
        return self._is_hole_visible

    @property
    def hole_card(self):
        return self.hands[0][Dealer.UPCARD_INDEX]

    # Setters

    @is_hole_visible.setter
    def is_hole_visible(self, b):
        self._is_hole_visible = b

    # Instance Methods (inherited from superclass)

    def print_hand(self):
        """Print the Dealer's hand.

        Prints '(HOLE CARD)' instead of the hole
        card if the hole card is not yet visible.

        """
        print("Dealer's cards: ")
        if not self.hands:
            print("No cards yet")

        elif self.is_hole_visible:
            super(Dealer, self).print_hand()
        else:
            for idx, card in enumerate(self.hands[0]):
                # substitute (HOLE CARD) instead of the info of the hole card
                p = '(HOLE CARD)' if idx == Dealer.HOLE_INDEX else card
                
                print('   ', p)

    def reset(self):
        """
        Resets Dealer for playing in another round (NOT another game).
        Empties hands and returns those cards for recycling.
        Resets bet to 0.
        """
        self.is_hole_visible = False
        return super(Dealer, self).reset()

    # Instance Methods (not inherited)

    def eligible_for_insurance(self):
        return self.hole_card.rank in\
                (Rank.ACE, Rank.TEN, Rank.JACK, Rank.QUEEN, Rank.KING)

    def show_cards(self):
        self.is_hole_visible = True
        self.print_hand()

class Player(BasePlayer):
    """
    Represents a Blackjack player.

    NB: Unlike in Dealer or the base class, self._hand refers to a list of 
    lists, each of which represents a hand. Property methods named hand and
    hands are added.
    """
    def __init__(self, cash):
        super(Player, self).__init__()
        self._bet = 0 # total bet in the current round
        self._cash = cash
        self._insurance = 0 # insurance bet

    # Properties

    @property
    def bet(self):
        return self._bet

    @property
    def cash(self):
        return self._cash

    @property
    def insurance(self):
        return self._insurance

    @property
    def all_cards(self):
        """ Returns flat list of all cards. """
        return list(chain.from_iterable(self._hands))

    @bet.setter
    def bet(self, bet):
        self._bet = bet

    @cash.setter
    def cash(self, cash):
        self._cash = cash

    @insurance.setter
    def insurance(self, insurance):
        self._insurance = insurance

    # Instance Methods (inherited from superclass)

    def reset(self):
        """ Resets Player

        Resets member variables for playing in another round (NOT another
        game). Empties hands and returns those cards for recycling. Resets bet
        to 0.

        """
        self._bet = 0
        self._insurance = 0
        return super(Player, self).reset()

    def print_hand(self, idx_hand=0, print_hand_num=True):
        """Print a single hand."""
        if print_hand_num:
            print('Player Hand #{}:'.format(idx_hand + 1))
        else:
            print('Player Hand:')

        super(Player, self).print_hand(idx_hand)

    # Instance Methods (not inherited)

    def discard_hand(self):
        self.hands = self.hands[1:]

    def payout_insurance(self, ratio):
        """Pays out insurance at the given ratio

        Rounds to the nearest dollar. Does not modify insurance; you will have
        to call reset later to zero out bet.
        """
        self.cash += self.insurance + int(round(self.insurance * ratio))

    def take_bet(self, bet):
        if bet <= self.cash:
            self.bet += bet
            self.cash -= bet
            return True
        else:
            return False

    def take_insurance(self, ins):
        self.insurance += ins
        self.cash -= ins

    def payout_bet(self, ratio=0):
        """Pays out bet at the given ratio.

        Rounds to the nearest dollar. Does not modify bet; you will have to
        call reset later to zero out bet.
        """
        self.cash += self.bet + int(round(self.bet * ratio))