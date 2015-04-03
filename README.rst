=====================
Tic-Tac-Toe in Django
=====================

Big Thanks to paulcwatts and his repo: https://github.com/paulcwatts/django-tictactoe

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