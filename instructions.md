TicTacToe
=========

A simple fun app for two players, X and O. You, the human, 'O', will play against the computer, 'X'.

Dependencies
------------

* Python 2.6 or later on the 2.x series.
* Django 1.6 or later on the 1.x series.
* Python packages in ``requirements/base.txt`` and ``requirements/local.txt``.

Getting Started
---------------

Set up virtual environment.

    In case you need to set up your virtual environment, run the following from the command line:

    $ easy_install pip
    $ pip install virtualenv
    $ pip install virtualenvwrapper
    $ cd ~/
    $ mkdir .virtualenvs

In your home directory edit the `.profile` or `.bash_profile` file and add the following:

    $ export WORKON_HOME=$HOME/.virtualenvs
    $ source /usr/local/bin/virtualenvwrapper.sh
    $ Save your .profile file and run: source ~/.profile or source ~/.bash_profile
    $ Done

Clone this repository
---------------------

    $ git clone git@github.com:percyperez/Tic-Tac-Toe.git

Create TicTacToe virtualenv project
-----------------------------------

    $ cd /path/to/tictactoe/
    $ mkvirtualenv tictactoe
    $ workon tictactoe
    $ pip install -r requirements/local.txt
    $ ./manage.py syncdb

Running the application
-----------------------

    $ cd /path/to/tictactoe/ and run the following:
    $ ./manage.py runserver localhost:8000
    $ Open a browser and go to http://localhost:8000
    $ To play, click on 'Computer start' or 'Human start' links

Running the tests
-----------------

If you want to run all tests, execute the following:

    $ ./manage.py test --settings=game.settings.test game.tictactoe.tests

If you want to run only the views tests, execute the following:

    $ ./manage.py test --settings=game.settings.test game.tictactoe.tests:TestView


NOTE: During the game, refreshing your browser will reset the game
