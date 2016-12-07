# X's & O's (Tic-Tac-Toe) Django App
### Requirements
 + Django >= 1.3
 + The X's & O's module (xsos.py)
 
### Installation
 + Ensure that the X's & O's module (xsos.py) and the tictactoe app (this package) are on your PYTHONPATH.
 + Ensure that `'django.contrib.sessions',` is in your installed apps and the sessions middleware is active.
 + Add `'tictactoe',` to your installed apps.
 + Add a route for tictactoe to your default urlconf.
   e.g. `url(r'^ttt/', include('tictactoe.urls')),`
 + Restart your webserver and play a game of X's & O's!

### Demo
A demo can be played at http://www.engineignite.com:8001/
