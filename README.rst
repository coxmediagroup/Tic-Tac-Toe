Intructions:
============

1. Fork this repo on GitHub. 
2. Create a program that can interactively play the game of Tic-Tac-Toe against
   a human player and never lose.
3. Commit early and often, with good messages. 
4. Push your code back to GitHub and send me a pull request.

We are a Django shop, but it is not a requirement that you implement your
program as a Django app.

(Don't be offended when I don't actually pull. I will clone your repo and
inspect it locally when I receive the request. This repo will be left
solution-less for obvious reasons.)

Response:
=========

Thanks for the opportunity to participate in this challenge. It's been a
blast. I've implemented a little djanog web-app with most of the UI
functionality implemented in javascript and jquery and the back-end done in
django, with json over ajax to communicate between.

Setting Up:
-----------

Clone the git repository to your local machine. You'll need to have either
setuptools_ or distribute_ installed in whatever python you use to build the
package, but as the entire thing is handled by zc.buildout you needn't worry
about anything beyond that.

If your environment is all set, run::

    $ python2.7 bootstrap.py
    ...
    Generated script '/blah/blah/Desktop/tictactoe/bin/buildout'.
    $ bin/buildout
    ...
    django: Skipping creating of project: tictactoe since it exists

And that is it. You'll be all set to go. Get the django site up and running
with::

    bin/django syncdb
    bin/django runserver

The database isn't really used for anything, but it's nice to know it's there,
don't you think?

You can run the minimal unit tests included with::

    bin/test

.. _setuptools: http://pypi.python.org/pypi/setuptools
.. _distribute: http://pypi.python.org/pypi/distribute