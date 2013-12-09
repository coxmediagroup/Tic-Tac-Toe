===================
Noughts and Crosses
===================
-------------------------------------------
Bryce Eggleton: Django & Python sample code
-------------------------------------------

This repo is meant to serve as sample code for a very simple Django/Python application.
So firstly, if you are an employer then let me thank you for taking the time to consider
me as a candidate for a position within your company.

I plan to expand upon this codebase in the near future since there
are a few very common constructs absent from this project including Python list
comprehension and database access through Django's ORM using models.

The goal is simple: create an interactive, browser-based game of tic-tac-toe, in which
a human plays against the computer. The computer can never lose (ending in a draw is
acceptable). I initially forked from `this code challenge. <//github.com/coxmediagroup/Tic-Tac-Toe>`_

There are further instructions below on how to quickly launch this project within an
instance of the Django dev server. If you are running Windows, there are also batch
files which can be run to take care of installing required Python packages as well
as running a local dev server.


Resume
------

You are welcome to contact me through LinkedIn, GitHub, or other avenues.
I try to keep my LinkedIn account the most current, however, so that would be
the best place to find up to date information.

`LinkedIn Profile for Bryce Eggleton <//www.linkedin.com/pub/bryce-eggleton/84/850/713>`_


Requirements
------------

To run this application on a local instance of the Django dev server, you must
have Python 2.7.5 and pip >= 1.4.1 installed properly.

For Windows, your /Python27 as well as /Python27/Scripts directories
**must** be included in the system path environment variable, otherwise the
setup batch file will fail.


Quickstart
==========

Windows
-------

1) run setup.cmd (django setup can take a couple minutes just give it a litte time)
2) run launchdev.cmd
3) navigate to ``127.0.0.1:8000`` in a browser
4) play noughts and crosses
5) close dev server
6) run uninstall.cmd


Linux
-----

Unfortunately I don't have any Linux installations right now, or I would have included
bash scripts as well, so instead, here are the shell commands which should allow a
fairly painless setup and launch. It is assumed that you are in the main project
directory for these commands.

Create a virtual environment::

    pip install virtualenvwrapper
    pip install --upgrade virtualenv
    mkvirtualenv test-bryce-eggleton
    workon test-bryce-eggleton

Install Python requirements::

    pip install -r requirements.txt

Launch the dev server::

    workon test-bryce-eggleton
    python manage.py runserver --settings=core.config

Remove Virtual Environment::

    deactivate
    rmvirtualenv test-bryce-eggleton


Shell Script Files
==================

setup.cmd
---------

This file will create a virtual environment for the Python packages this
project requires so as not to pollute your main Python installation.
Then it will install any required Python packages for the project, including
Django into the virtual environment. At that point, the project should be
completely configured and ready to run, via the next script.


runserver.cmd
-------------

This will launch an instance of the Django dev server with the project
settings and at that point, an interactive game of Noughts and Crosses
will be available from your browser at ``127.0.0.1:8000``


uninstall.cmd
-------------

This file simply removes the virtual environment created from the setup.cmd
script to leave almost no trace of the project.


TODO
====

#) add samples for list comprehension and models/ORM
#) migrate to a clean, non-forked repo
#) darken out board a bit once the game is over
#) make the game status text more prominent
#) highlight what each player's last move was

