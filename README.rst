================================
 CMG Tic-tac-toe Code Challenge
================================

Intructions
-----------

1. Fork this repo on GitHub.
2. Create a program that can interactively play the game of Tic-Tac-Toe against
   a human player and never lose.
3. Commit early and often, with good messages.
4. Push your code back to GitHub and send me a pull request.

If you don't want to broadcast your intentions by forking this, feel free to
clone it and work locally. Then, send us a tar.gz of your solution, including
your .git folder so we can see your commit history.

We are a Django shop, but it is not a requirement that you implement your
program as a Django app.

(Don't be offended when I don't actually pull. I will clone your repo and
inspect it locally when I receive the request. This repo will be left
solution-less for obvious reasons.)


Installation & Setup
--------------------

1. ``git clone git://github.com/benspaulding/Tic-Tac-Toe.git``
2. Create a virtual environment or add the new ``Tic-Tac-Toe`` directory to
   your current one.
3. ``cd Tic-Tac-Toe/``
4. ``pip install -r requirements.txt``
5. ``./manage.py test tictactoe``
6. ``./manage.py syncdb``
7. ``./manage.py runserver``
8. Open a browser and try it out!


Ben’s TODO
----------

Along with the FIXME and TODO notes in the code:

* Make grid recognize a win, a draw, and an in-progress game.
* Create custom manager for game to access games based on status.
* Install South.
* Write initial data migration. (Setup my user, site, etc.)
* Add travis-ci support.
