Setup
=====
* Setup SQLite database models by navigating to project directory and typing the command 'python manage.py sql tictactoe'
* Sync Models to SQLite database by typing command 'python manage.py syncdb'
* Start "Tic Tac Taco" by typing command 'python manage.py runserver 8080'
** Note that for production, a uWSGI interface would be implemented but falls outside the scope of this assignment

Game
====
Welcome to Tic Tac Taco!

If you manage to beat the computer you win a free year's supply of tacos! First player is chosen randomly. Simply enter in your email address to start or continue your game!

AI algorithm "borrowed" from: https://gist.github.com/SudhagarS/3942029

Story
======

As a CMG manager, I want to see how you code a game of Tic Tac Toe, so that I can get a feel for a candidate's skills and strengths.

Acceptance criteria
=======================

* The AI should never lose
* The submission must include both server & client side code -- no CLI-only or browser-only implementations. Play to your strengths, but show us your full range of skills.
* Quality counts! A good submission that takes a while is better than a poor submission quickly.
* You should include clear instructions for how to run your application


Technical notes
------------------

* We are a Django shop, but it is not a requirement that you implement your program as a Django app.
* Make sure your submission accurately reflects your development style.
* Commit early and often, with good messages.


Submissions
---------------

1. Publicly: Fork this repo and send us a pull request.
2. Privately: Send us a tar.gz of your solution **including your .git folder** so we can see your commit history.

