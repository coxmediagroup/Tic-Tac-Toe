django-tic-tac-toe
=================

Installation
------------

The installation of this software assumes you posses a working knowledge of
virtualenv_, limited exposure to python web development, and are familiar with
the operation of the shell application appropriate for your operating system.

This software was tested on, and known to work on, **Python 2.7.3** and **3.2.3**.

.. note: Examples shown assume you are working with a UNIX-style shell (OSX,
         Linux, etc) rather than a cmd-style (``cmd``, ``powershell``, etc)
         like those found on Windows systems. For Windows systems, you may have
         to adjust references to directory paths.

The installation steps required are fairly minimal.

In a terminal, create a new virtualenv for the project::

    $ virtualenv /tmp/demo

Activate the virtualenv::

    $ source /tmp/demo/bin/activate

Install the required python packages for the project::

    $ pip install -r requirements.txt

Then finally, create the database for the project by issuing::

    $ python manage.py syncdb


What follows is a log (including all the output) from a terminal session where
I perform these steps. You should see similar, but not necessarily identical,
output if the steps are performed correctly.

::

    owen@gaff:~/projects/Tic-Tac-Toe$ virtualenv /tmp/demo
    New python executable in /tmp/demo/bin/python
    Installing setuptools............done.
    Installing pip...............done.
    owen@gaff:~/projects/Tic-Tac-Toe$ source /tmp/demo/bin/activate
    (demo)owen@gaff:~/projects/Tic-Tac-Toe$ pip install -r requirements.txt
    Downloading/unpacking Django==1.5.1 (from -r requirements.txt (line 1))
      Downloading Django-1.5.1.tar.gz (8.0MB): 8.0MB downloaded
      Running setup.py egg_info for package Django

        warning: no previously-included files matching '__pycache__' found under directory '*'
        warning: no previously-included files matching '*.py[co]' found under directory '*'
    Requirement already satisfied (use --upgrade to upgrade): argparse==1.2.1 in /usr/lib/python2.7 (from -r requirements.txt (line 2))
    Requirement already satisfied (use --upgrade to upgrade): wsgiref==0.1.2 in /usr/lib/python2.7 (from -r requirements.txt (line 3))
    Installing collected packages: Django
      Running setup.py install for Django
        changing mode of build/scripts-2.7/django-admin.py from 664 to 775

        warning: no previously-included files matching '__pycache__' found under directory '*'
        warning: no previously-included files matching '*.py[co]' found under directory '*'
        changing mode of /tmp/demo/bin/django-admin.py to 775
    Successfully installed Django
    Cleaning up...
    (demo)owen@gaff:~/projects/Tic-Tac-Toe$ python manage.py syncdb
    Creating tables ...
    Installing custom SQL ...
    Installing indexes ...
    Installed 0 object(s) from 0 fixture(s)


The tic-tac-toe django app comes with a set of unit tests that you can run to
verify that the project requirements are all in place.

You can run the test suite by issuing: ``python manage.py test tictactoe``.

For example::

    (demo)owen@gaff:~/projects/Tic-Tac-Toe$ python manage.py test tictactoe
    Creating test database for alias 'default'...
    .............
    ----------------------------------------------------------------------
    Ran 13 tests in 0.001s

    OK
    Destroying test database for alias 'default'...



How To Play
-----------

Web
^^^

With your virtualenv activated, issue the command ``python manage.py runserver``::

    (demo)owen@gaff:~/projects/Tic-Tac-Toe$ python manage.py runserver
    Validating models...

    0 errors found
    May 25, 2013 - 14:33:21
    Django version 1.5.1, using settings 'main.settings'
    Development server is running at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

The web server should now be running the application. You should now be able to
visit http://127.0.0.1:8000/ in your browser to play the game.

The game stores game-state using the browser session so you should be able to
abandon, and later resume, a game in progress.

It's also worth noting that the game uses javascript to communicate state
changes between the server and client, however this is a progressive enhancement
designed to reduce response time, and number of requests made to the server.
You should have a *virtually identical* game experience should you choose to
disable javascript in your browser.

CLI
^^^

There is also a cli game, but this is far less polished. It was designed
primarily for my prototyping process to verify the board logic.

To start a game, issue ``python manage.py play_game`` in your terminal.

Once the game has begun, you may mark cells by entering their 0-based
numbers (0-8).

``CTRL-C`` can be used to quit a game in progress.

.. _virtualenv: https://virtualenv.readthedocs.org/en/latest/
