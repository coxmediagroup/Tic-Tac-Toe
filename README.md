Overview
========
This is an app that plays the game of tic-tac-toe; human vs AI.  
 * The human's user interface is a web browser.  The AI engine's interface is a web service.
 * The browser and web service interact by exchanging an evolving tic-tac-toe board state.
 * All game logic is performed by the web service; the browser's responsibilities are simply:
  1. collect user prefs (e.g. who goes first),
  2. display the current board state,
  3. change the board state when user clicks on an empty cell,
  4. send the new board state to the web service, and
  5. display the web service's response (either the new board state or "game over" details)

###Requirements
 * Python 3.x

###Features
 * Few dependencies
  - Python 3.x
  - JavaScript enabled in browser
  - modern browser (IE8+)
 * Single Page Application

###Shortcomings
 * Mouse only
 * IE8+

Installation/Setup Instructions
-------------------------------
The following assumes that you're running a Debian variant of Linux.
If you're not, you'll need to make the appropriate changes (e.g. use **yum** instead of **apt**).

####1. Clone (or download) this repo

####2. Install Python 3.x
Chances are that you already have Python 3 installed.  Here's how to find out...

```
$ python --version
Python 3.4.3
```

####3. Start the web server
cd to the project root directory and enter the following
```
python server/tictactoe_server.py
```

You should then see something like...
```
[Mon Mar  9 14:13:34 2015] Server started on :9000
```

Note: to stop the server, type `ctrl+c` (^C)

####4. Run the unit tests
From a different terminal window, and again from the project root...
```
python -m unittest
```

You should then see something like...

```
....
----------------------------------------------------------------------
Ran 4 tests in 4.398s

OK
```

####5. Play the game!

http://localhost:9000

###Config parameters (server host, port, etc.)
All configuration variables are stored in `server/config.ini`.  

```
[DEFAULT]
# listen on all interfaces
host_name =
host_port = 9000

[TESTS]
number_of_ai_vs_ai_games = 10
number_of_ai_vs_random_games = 25
```

This file is used by both the server and unit tests.

Technical Notes
---------------
This solution was designed to be "just right" for the assignment (e.g. No
client-side or server-side frameworks were needed so none were used).

###The Game Board
The game board is represented as a 9 character string, where characters 0-2
represent the top row of the board, characters 3-5 represent the middle row,
and characters 6-8 represent the bottom row, e.g.

```
0 1 2
3 4 5
6 7 8
```

Each character will always have 1 of 3 values:

Character | Meaning
--------- | -------
`X`       | position occupied by Human player
`O`       | position occupied by AI player
`-`       | position unoccupied

So if the board state was this...

```
X O X
O   X
X O
```

...the board string would be `XOXO-XXO-`

At the start of the game all positions are unoccupied, making the board string `---------`.

###Performance
Because...
 1. the server is stateless (i.e. the entire board state is passed in each request), and
 2. each response takes roughly the same amount of time to calculate, and
 3. the user will introduce latency as he/she selects the next move,

...Python's simple, single-threaded web server (`http.server`) is used and should be able to provide
acceptable performance for hundreds of simultaneous users, even if deployed on commodity-level hardware.


Code components/structure
-------------------------
This is a Single Page Web Application, the frontend (client) running in the browser
interacting with the backend (server) via AJAX.  The frontend is responsible for
presenting the board and interacting with the user; the backend houses the AI and
is responsible for evaluating the board (e.g. determining if there is a winner or a
draw) and making new moves.

###Server/backend
The server is comprised of the three files in the `Tic-Tac-Toe/server` subdirectory:
 * `server.py` - based on the http.server module of the python 3 standard library,
   handles http GET and HEAD requests, serves static files, and provides a request
   handler class (`DynamicContentRequestHandler`) which may be subclassed to
   serve dynamic content.

 * `tictactoe_server.py` - the actual backend server.  Subclasses `DynamicContentRequestHandler`
   from `server.py` and provides the sole backend endpoint: `evalBoard`

 * `tictactoe_ai.py` - houses the actual AI and is imported by `tictactoe_server.py`.
   Performs these tasks:
   1. determines if the game is over and if so who won (or if a draw), and
   2. makes the next move for the AI player.


###Client/frontend
The client is comprised of the files in the `Tic-Tac-Toe/static` subdirectory.  All
frontend application logic resides in `tictactoe.js`.

###Unit Tests
The unit tests reside in the `Tic-Tac-Toe/tests` subdirectory.  Only the server has
test scripts.
