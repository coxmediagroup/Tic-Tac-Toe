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


###Features
 * Few dependencies
  - python3.4
  - JavaScript enabled in browser
  - modern browser (IE8+)
 * Single Page Application

###Shortcomings
 * Mouse only
 * Not Accessibility Friendly
 * IE8+

Technical Notes
---------------
This solution was designed to be "just right" for the assignment (e.g. No
client-side or server-side frameworks were needed so none were used).

###The Game Board

###Performance
Because...
 1. the server is stateless (i.e. the entire board state is passed in each request), and
 2. each response takes roughly the same amount of time to calculate, and
 3. the user will introduce latency as he/she selects the next move,

...Python's simple, single-threaded web server (`http.server`) is used and should be able to provide
acceptable performance for hundreds of simultaneous users, even if deployed on commodity-level hardware.


Requirements
------------
 * python 3.x

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



Code components/structure
-------------------------
