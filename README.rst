Tic-Tac-Toe
===========
This is tic-tac-toe_ as a client-server Django app.

The user loads the front page, and clicks a button to decide if they want to
go first ('X') or second ('O').  The user and the app take turns adding X's
and O's to a three-by-three grid until the app wins.  The user can then
start a new game.

Getting Started
---------------
1. Create a virtualenv_
2. Install requirements: `pip install -r requirements.txt`
3. Run it: `./manage.py runserver`
4. Play it: `http://localhost:8000/ <http://localhost:8000>`

If you are developing, you may want to install the additional requirements
in `requirements.dev.txt`, and customize settings with `local_settings.py`.

Purpose
-------
This project was created as a `programming exercise`_ for a `job application`_.
The requirements are:

* The AI should never lose
* The submission must include both server & client side code -- no CLI-only
  or browser-only implementations.
* Quality counts! A good submission that takes a while is better than a poor
  submission quickly.
* You should include clear instructions for how to run your application

When I was first recruited, I was too busy to write code, but I did have about
2 months to think about the problem before I started.

.. _`job application`: http://cmgd-jobs.readthedocs.org
        /en/latest/developer.html
.. _`programming exercise`: https://github.com/coxmediagroup/Tic-Tac-Toe
.. _`tic-tac-toe`: http://en.wikipedia.org/wiki/Tic-tac-toe
.. _virtualenv: http://virtualenvwrapper.readthedocs.org/en/latest/
