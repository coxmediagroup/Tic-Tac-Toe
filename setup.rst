SETUP
=====

Create a virtualenv::

    mkvirtualenv tictactoe_env

Install requirements::

    pip install -r requirements.txt

Create database (for django session store)::

    python tictactoe/manage.py syncdb

Start the django web server::

    python tictactoe/manage.py runserver

Open your browser to http://127.0.0.1:8000 and play Tic-Tac-Toe
