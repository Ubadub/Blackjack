# Information

A single-player blackjack game. You play against the house (the dealer).

# Instructions for running

To run this game, you need Python 3.7. No third-party libraries are required. Note: This has been definitively confirmed as working for Python 3.7+ but will likely run on 3.3+.

Once you're in the program's directory, just run `Blackjack.py` with python3. The program will open with a set of instructions for interacting with it.

# Explanation of Design Choices

I elected to use Python because it is the language I am most familiar with. I broke up the program into several classes: `Deck`, `Card`, `BasePlayer`, `Dealer`, `Player`, and `Blackjack`.

One of the issues I faced was deciding how to relate `Player` and `Dealer`. In the end, in the interests of not repeating code and saving time, I decided to make them both subclasses of the same superclass, `BasePlayer`.

I also used several `Enums` to store certain constants that are important for storing game state. For example, the `Moves` enum encompasses the various commands that a user can type into the terminal.

You may notice that I've written the program as if a player could have multiple hands at a time. The purpose of this is to allow users to choose to split their cards into two hands. This is a standard feature of most blackjack games. Because of time constraints, I was unable to develop this feature in full. Nonetheless, most of the underlying architecture is intact despite the game behaving, from the perspective of the user, as if you could only play one hand at a time.

During the execution of the game, I invoke `time.sleep()` at certain key junctures to prevent too much text from appearing on the computer at once.

Regrettably, due to the time constraints, I was not able to spin up a proper test framework.
