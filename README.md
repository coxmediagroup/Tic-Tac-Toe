# Tic-Tac-Toe
## Code test for Cox Media Group.

This project has been built and tested on Python 2.7.1 and Django 1.3.1.

The game implementation is stored in the game.py module.  The strategy is a
defensive one, based on the Minimax algorithm.
    http://en.wikipedia.org/wiki/Minimax

A basic unittest that iterates over every possible game is in tests.py,

In addition, a Django interface for the game is included.  To run, install
dependencies (ideally into a virtual environment):

    pip install -r requirements.txt

The default project configuration has dependencies on sqlite3 for session
management.  Game state is stored in the (anonymous) user session.
