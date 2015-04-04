=====================
Tic-Tac-Toe in Django
=====================

Big Thanks to [paulcwatts](https://github.com/paulcwatts/django-tictactoe) and his repo
Big Thanks to [Cecil Woebker](http://cwoebker.com/posts/tic-tac-toe), and [Maurits van der Schee](http://www.leaseweblabs.com/2013/12/python-tictactoe-tk-minimax-ai/)

Building
--------

The easiest way to get this set up is to use virtualenv_. Usually it's easy as::

    sudo pip install virtualenv

Once you have virtualenv and the code, you can create a virtualenv and install the dependencies::

    cd <path_to_code>
    mkvirtualenv tictactoe
    pip install -r requirements.txt
    python manage.py syncdb

Then run the server::

    python manage.py runserver

To run the tests:

    python manage.py test