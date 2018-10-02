from enum import Enum
import math
import time

from Card import *
from Deck import *
from Player import *

# Payout Ratios expressed as two numbers for printing purposes
# 3:2 payout for a natural blackjack
BLACKJACK_PAYOUT_NUM = 3
BLACKJACK_PAYOUT_DENOM = 2

# 2:1 payout for insurance
INSURANCE_PAYOUT_NUM = 2
INSURANCE_PAYOUT_DENOM = 1

MIN_BET = 10
MAX_BET = 100

STARTING_CASH = 1000

class Moves(Enum):
    STAND = 'stand'
    HIT = 'hit'
    DOUBLE = 'double'
    SURRENDER = 'surrender'
    HELP = 'help'

    def __repr__(self):
        return self.name

# Mapping between possible moves and what the user can type to trigger them.
# Case insensitive.
MOVE_CMDS = {
    **dict.fromkeys(['stand', 's'], Moves.STAND),
    **dict.fromkeys(['hit', 'h'], Moves.HIT),
    **dict.fromkeys(['double', 'd'], Moves.DOUBLE),
    **dict.fromkeys(['surrender', 'su'], Moves.SURRENDER),
    **dict.fromkeys(['help', '?'], Moves.HELP),
}

class Blackjack():
    """ Represents a game of Blackjack. """

    def __init__(self):
        self._dealer = Dealer()
        self._deck = Deck()
        self._player = Player(STARTING_CASH)

    # Static Methods

    @staticmethod
    def get_move_from_txt(txt):
        """
        Returns the move associated with the given text command, or
        None if no such association exists.
        """
        return MOVE_CMDS.get(txt.lower())

    @staticmethod
    def help_screen():
        """
        Prints a help screen containing info about the commands one can use in
        this game.
        """
        print("\n\nWelcome to the game of Blackjack!",
            "\nHere is a list of commands you can type followed by an",
            "explanation of what they do. Commands that have the same",
            "function are listed on the same line separated by commas.",
            "Please note that not all commands can be entered at any given",
            "time. All commands are case insensitive.",

            "\n",

            "\nhelp, ?:",
            "\t\tBrings up this help screen.",

            "\n",

            "\nstand, s:",
            "\t\tStand, passing your turn.",

            "\n",

            "\nhit, h:",
            "\t\tHit. The dealer will give you a card.",

            "\n",

            "\ndouble, d:",
            "\t\tDouble down on your bet. You will be asked to bet",
            "\n\t\t\tan amount no greater than your initial bet, and then you will",
            "\n\t\t\tbe dealt one, and only one, more card.",

            "\n",

            "\nsurrender, s:",
            "\t\tForfeit after being dealt your first two cards.",
            "\n\t\t\tHalf of your bet will be returned to you.\n\n\n\n"
            )

    # Properties

    @property
    def dealer(self):
        return self._dealer

    @property
    def deck(self):
        return self._deck

    @property
    def player(self):
        return self._player

    @deck.setter
    def deck(self, val):
        self._deck = val

    # Instance Methods
    def burn(self):
        """Discards the top card, as is the tradition in many casinos."""
        self.deck.draw()

    def deal_dealer(self, n=1):
        self.dealer.deal(self.deck.draw(n))

    def deal_player(self, n=1, idx_hand=0):
        self.player.deal(self.deck.draw(n), idx_hand)

    def dealer_play(self):
        print("The dealer plays...")
        time.sleep(.5)

        print("The dealer flips over his hole card.")
        time.sleep(.5)
        self.dealer.show_cards()

        while self.dealer.score() < 17:
            time.sleep(1)
            print("The dealer deals a card to himself...")
            self.deal_dealer()
            self.dealer.print_hand()

        time.sleep(1)
        print("The dealer finishes.")

    def get_player_move(self, valid_moves=list(Moves), msg="Your move: "):
        while True:
            # player_move = input("Your move. You can stand or hit.")
            # TO DO: Dynamic string based on valid moves
            m = Blackjack.get_move_from_txt(input(msg))
            if m:
                if m == Moves.HELP:
                    self.help_screen()
                elif m in valid_moves:
                    return m
                else:
                    print("You can't {} now.\n".format(m.value))
            else:
                print("That's not a valid move command.\n")

    def handle_insurance(self):
        """ Asks the Player if they want insurance.

        This can only happen when the dealer's faceup card is an ace, ten, or
        a face card.

        """
        print("Do you want insurance? If the dealer has a natural blackjack,",
            "then you will be paid",
            INSURANCE_PAYOUT_NUM, 'to', INSURANCE_PAYOUT_DENOM,
            "on your insurance.\nOtherwise, you",
            "forfeit the insurance amount.")

        s = input("Type y to take insurance or press any other key to skip it: ")
        if s.lower() == 'y':
            insurance_max = int(math.floor(self.player.bet/2))
            amt = self.get_bet_amount(min_bet=1, max_bet=insurance_max,
                    msg="Your insurance bet can be up to half of your original bet.")
            self.player.take_insurance(amt)

    def hit(self, idx_hand=0):
        self.deal_player(idx_hand = idx_hand)
        print("Dealer deals you a card. Your hand is now:")
        self.player.print_all_hands()

    def reset(self):
        self.player.reset()
        self.dealer.reset()
        self.deck = Deck()

    def get_bet_amount(self, min_bet=MIN_BET, max_bet=MAX_BET, msg=None):
        cash = self.player.cash

        max_bet = min(cash, max_bet)
        if not msg:
            msg = ("You have ${}. You must bet at least ${} and no more than ${}. "
                    "You must bet a whole number.\n").format(cash,
                                                            min_bet,
                                                            max_bet)

        print(msg)
        while True:
            try:
                bet = int(input("How much would you like to bet? "))
                if bet < min_bet:
                    print("Sorry your bet is not high enough.\n")
                elif bet > max_bet:
                    print("Sorry your bet is too high.\n")
                elif bet > self.player.cash:
                    print("Sorry you don't have that much cash.\n")
                else:
                    print()
                    break
            except ValueError as e:
                print("Invalid bet (you must bet a whole number).\n")

        return bet

    def take_bet(self, min_bet=MIN_BET, max_bet=MAX_BET):
        self.player.take_bet(self.get_bet_amount(min_bet, max_bet))

    def payout_blackjack(self):
        print("Blackjack! You will be paid out at {}:{}.\n".
                format(BLACKJACK_PAYOUT_NUM, BLACKJACK_PAYOUT_DENOM))

        self.player.payout_bet(BLACKJACK_PAYOUT_NUM/BLACKJACK_PAYOUT_DENOM)

    def payout_insurance(self):
        print("Your insurance will be paid out at {}:{}.\n".
                format(INSURANCE_PAYOUT_NUM,INSURANCE_PAYOUT_DENOM))
        self.player.payout_insurance()

    def payout_tie(self):
        print("You tied with the dealer. Your bet will be returned to you.\n")
        self.player.payout_bet()

    def payout_win(self):
        print("You will be paid out 1:1.\n")
        self.player.payout_bet(1)

    def check_blackjack(self):
        player_blackjack = self.player.score() == 21
        dealer_blackjack = self.dealer.score() == 21

        if dealer_blackjack:
            print("\nThe dealer Blackjacked!\n")
            self.dealer.show_cards()

            if self.player.insurance:
                self.payout_insurance()

            if player_blackjack: # Return bet, end round
                self.payout_tie() # return original bet
                return True
            else: # Player loses bet, end round
                print("You lose your bet...\n")
                return True
        else:
            if self.player.insurance:
                print("You've lost your insurance.\n")

            if player_blackjack: # Pay player and end round
                self.payout_blackjack()
                return True
            else: # No one blackjacked
                return False

    def play(self):
        """ The game loop. """
        while self.player.cash >= MIN_BET:
            self.take_bet()

            print("The top card will now be burned...")
            self.burn()

            print("Dealing...")
            # Deal first two cards, starting with Player to the left of Dealer
            for i in range(2):
                self.deal_player()
                self.deal_dealer()

            time.sleep(1)
            self.player.print_hand()
            time.sleep(1)
            self.dealer.print_hand()

            if self.dealer.eligible_for_insurance():
                self.handle_insurance()

            # Check blackjack
            if self.check_blackjack():
                self.reset()
                continue

            # Ask for moves for each Player hand before Dealer does anything
            print()
            valid_moves = [Moves.STAND, Moves.HIT, Moves.SURRENDER, Moves.HELP]
            if self.player.bet < self.player.cash: # can double bet
                valid_moves.append(Moves.DOUBLE)
            hand = self.player.get_hand()

            m = self.get_player_move(valid_moves = valid_moves)
            # We do nothing if the player stands
            # Hit: keep asking if player wants to hit
            if m == Moves.HIT:
                bet = self.player.bet
                print("You bet ${}.".format(bet))
                self.player.take_bet(bet)
                self.hit()
                while self.player.score() < 21:
                    m = self.get_player_move(
                            valid_moves = [Moves.STAND, Moves.HIT, Moves.HELP],
                            msg = 'Hit or stand? ')
                    if m == Moves.HIT:
                        self.hit()
                    elif m == Moves.STAND: # Player stands
                        break
                    else:
                        help_screen()

            elif m == Moves.DOUBLE:
                self.player.take_bet(self.player.bet)
                self.hit()
                
            elif m == Moves.SURRENDER:
                print("Half of your bet will be returned.\n")
                self.player.payout_bet(-.5)
                self.reset()
                continue

            p_score = self.player.score()

            # If you bust out, auto-lose round
            if p_score > 21:
                print("Oops! You've busted. Discarding hand...\n")

            # Otherwise, the dealer plays
            else:
                self.dealer_play()
                
                d_score = self.dealer.score()
                print("Your score:", p_score)
                print("Dealer's score:", d_score)

                if d_score == p_score:
                    self.payout_tie()
                elif d_score > 21:
                    print("The dealer busted!\n")
                    self.payout_win()
                elif d_score > p_score:
                    print("The dealer beat you!\n")
                elif d_score < p_score:
                    self.payout_win()

            self.reset()
        else: 
            print("You have insufficient cash to play!")
        

def main():
    game = Blackjack()
    game.help_screen()
    game.play()

if __name__ == '__main__':
    main() 