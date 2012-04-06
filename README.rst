.. _README:

README
======

Overview
--------

Tic Tac Toe is a Django web application for playing the classic board game
in a user's web browser. It currently supports game boards from the sizes of
3X3 to 9X9 and has a rudimentary/unoptimized implementation of the Minimax
algorithm for the computer AI.

Components
----------

Game
~~~~~
Functionality for playing the actual game of Tic Tac Toe. It allows for the
board's creation, the CPU AI, and the player's movements.

The Game Board will use AJAX to update itself if javascript is enabled but
does correctly fall-back to a normal post if disabled.

System Dependencies
-------------------

There are no network dependencies at this time. For installation, please see
DEPLOYNOTES.rst.

-----

For more detailed information, including installation instructions and upgrade
notes, see DEPLOYNOTES.rst.  For details about the features included in each release,
see CHANGELOG.rst.