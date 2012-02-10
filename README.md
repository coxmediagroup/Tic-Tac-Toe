Tic-Tac-Toe
===========
Play Tic-Tac-Toe against a computer via a Django-web interface.

Dependencies
------------
This project has been built and tested on Python 2.7.1 and Django 1.3.1.

    $ pip install -r requirements.txt

Details
-------
The game implementation is stored in the `game.py` module.  The strategy is a
defensive one, based on the [Minimax](http://en.wikipedia.org/wiki/Minimax)
algorithm.

A basic unittest that iterates over every possible game is in `tests.py`:

    $ ./tests.py

The default project configuration has dependencies on sqlite3 for session
management; game state is stored in the (anonymous) user session.  Therefore,
you must create a database:

    $ ./manage.py syncdb

Then, to run the Django dev server:

    $ ./manage.py runserver
