CMG Tic-Tac-Toe
===============

A Tic-Tac-Toe app for CMG consideration. The app is built with Django, Twitter-Bootstrap, and jQuery. 
This app is fully responsive, includes a minimax AI that never loses, and a high-score board.

Installation
============

To install this app, first clone the repository:

```
git clone https://github.com/zebulasampedro/Tic-Tac-Toe.git
```

Then, install the required packages:
*It is recommended that this step be done in a virtualenv with no-site-packages, to avoid conflicts with existing packages.*

```
pip install -r Tic-Tac-Toe/tictactoe/requirements.txt
```

In the app root, collect the static files:

```
python manage.py collectstatic
```

Sync the database:

```
python manage.py syncdb
```

Finally, run the server:

```
python manage.py runserver 0.0.0.0:8000
```

The app will now be accessible at http://<your-host>:8000/tictactoe/!



