Otterson Tic-Tac-Toe example.
=============================

I don't have Django installed on my web box at home, but I do have Python.

I coded this as a HTML5/CSS/Javascript front end, with a Python web service,
written as a simple CGI, as the back end.  

The web service accepts a HTTP GET request
containing a "board" parameter which is the the current state of the Tic-Tac-Toe
playing field, represented as a string of 9 digits: 0 for empty, 1 or 2 for a
played square, and a "computer" parameter, which contains a single digit that
represents the player number of the computer.

The web service returns a JSON document.  The document may contain any of the 
following fields:

* error - an error message.
* winner - a digit representing the winner, 0, no winner, or 3 for a draw.
* board - the board string, as described above.  useful if the client keeps no state.
* player - the computer player number.  useful if the client keeps no state.
* move - the square number of the square taken by the computer.

The client is on-the-metal.  There are no frameworks used.

There is a working demonstration available at http://test.n1kdo.com/tictac.html

