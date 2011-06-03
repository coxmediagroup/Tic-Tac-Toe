#X's & O's (Tic Tac Toe)

### About
The Python module xsos.py contains an interactive version of X's and O's where the player can choose which mark (X or O) the computer controls.

X always goes first (see http://en.wikipedia.org/wiki/Tic-tac-toe) and the computer will never lose.

### Usage
To play a game simply run xsos.py from the command line with `python xsos.py` from the directory that contains xsos.py

To simulate a set of games run sim.py with the number of games to play, e.g. `python sim.py 1000` from the directory that contains sim.py

To execute the doctests run tests.py, e.g. `python tests.py` from the directory that contains tests.py

## Django App

### About
A simple Django application is included in the package `tictactoe`. It uses Django's built in sessions to track the game progress.

It currently only supports playing against the computer but the user may choose to play as either X or O.

### Requirements
 + Django >= 1.3
 + The X's & O's module (xsos.py)
 
### Installation
 + Ensure that the X's & O's module (xsos.py) and the tictactoe app (this package) are on your PYTHONPATH.
 + Ensure that `'django.contrib.sessions',` is in your installed apps and the sessions middleware is active.
 + Add `'tictactoe',` to your installed apps.
 + Add a route for tictactoe to your default urlconf.
   e.g. `url(r'^ttt/', include('tictactoe.urls')),`
 + Restart your webserver and play a game of X's & O's!
