# Challenge Complete! Again!

The first iteration I had of this project I did as an Angular SPA app. The
line in the README "it is not a requirement that you implement your 
program as a Django app" and possibly some other factors led me to think
I should do the app in Angular.

The first iteration also would sometimes lose. I implemented the
[algorithm from Wikipedia incorrectly](http://en.wikipedia.org/wiki/Tic_tac_toe#Strategy).

Since the first interview I took the following steps:

1. Algorithm never loses, it will always at least draw
1. Added a [Wargames](http://en.wikipedia.org/wiki/WOPR) reference
1. Restructured the project as a Django app, but still using Karma to test the angular components (wrapped in a Django unit test, so it's one command to test)
1. You can now permalink to a specific move in a game
1. Games are POST'ed back to the server (not 100% RESTful, a little hurried), times and IP addresses are stored, it could be interesting to map players' locations and analyze response times
1. An admin backend allows you to browse game history (will email a username and password)
1. To replace Yeoman/Grunt/uglify I implemented [django-compressor](http://django-compressor.readthedocs.org/en/latest/)

# Installation

I use virtualenv for everything. Here's how to setup if you want to try running locally:
    
    $ virtualenv --no-site-packages ~/virtualenvs/t3
    # ( or similar )

    $ source ~/virtualenvs/t3/bin/activate
    
    $ git clone https://github.com/jdillworth/tic_tac_toe
    $ cd tic_tac_toe/
    $ pip install -r requirements.txt 

    # now install Node components
    $ cd tictactoe/static/tictactoe/ng/
    $ npm install

    # back to project root
    $ cd ../../../../
    $ ./manage.py syncdb
    $ ./manage.py migrate
    $ ./manage.py runserver
    $ ./manage.py test tictactoe

You'll also need to setup site 1 in the admin (at /mgmt/) with the protocol and name
e.g. "http://localhost:8000/". In retrospect I see this is a bit wrong. I've patched
my code to work without the http://, so that's at least a bit more standard.

