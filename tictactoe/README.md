# X's & O's (Tic-Tac-Toe) Django App

### Installation
 + Ensure that the X's & O's module (xsos.py) is on your PYTHONPATH.
 + Ensure that `'django.contrib.sessions',` is in your installed apps.
 + Add `'tictactoe',` to your installed apps.
 + Add a route for tictactoe to your default urlconf.
   e.g. `url(r'^ttt/', include('tictactoe.urls')),`
 + Restart your webserver and play a game of X's & O's!