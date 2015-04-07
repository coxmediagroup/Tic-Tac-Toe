=====================
Tic-Tac-Toe in Django
=====================

Big Thanks to [paulcwatts](https://github.com/paulcwatts/django-tictactoe) and his repo
Big Thanks to [Cecil Woebker](http://cwoebker.com/posts/tic-tac-toe), and [Maurits van der Schee](http://www.leaseweblabs.com/2013/12/python-tictactoe-tk-minimax-ai/)

Building
--------
So far it has been tested for manage.py

    cd <path_to_code>
    pip install -r requirements.txt
    python manage.py syncdb
    python manage.py migrate  # This will create the game table in case syncdb failed 

Then run the server::

    python manage.py runserver

To run the tests:

    python manage.py test
