================================
 CMG Tic-tac-toe Code Challenge
================================

Instructions
------------

1. Fork this repo on GitHub.
2. Create a program that can interactively play the game of Tic-Tac-Toe against
   a human player and never lose.
3. Commit early and often, with good messages.
4. Push your code back to GitHub and send me a pull request.


Ben’s Notes
-----------

This Django app allows a person to play Tic-tac-toe against the program, and
the program will never lose — mission accomplished! There are still
improvements I would like to make, but the app functions as-is. Have a look at
the code to see how it all works, what I want to improve, and all that good
stuff.


Installation & Setup
~~~~~~~~~~~~~~~~~~~~

1. ``git clone git://github.com/benspaulding/Tic-Tac-Toe.git``
2. Create a virtual environment or add the new ``Tic-Tac-Toe`` directory to
   your current one.
3. ``cd Tic-Tac-Toe/``
4. ``pip install -r requirements.txt``
5. ``./manage.py test tictactoe``
6. ``./manage.py syncdb``
7. ``./manage.py runserver``
8. Open a browser and try it out!


TODO
~~~~

Along with the FIXME and TODO notes in the code:

* Make a better interface for submitting a turn. (Multiple form fields instead
  of the current ascii grid.)
* Make grid recognize a win, a draw, and an in-progress game.
* Create custom manager for game to access games based on status.
* Install South.
* Write initial data migration. (Setup my user, site, etc.)
* Add travis-ci support.
