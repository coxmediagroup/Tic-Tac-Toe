=============
Tic Tac Toe
=============
:Author:
	Eric Ressler, 
	eric.k.ressler@gmail.com
:Version: 1.0
:Date: July 5, 2014

Installation Instructions
--------------------------

* Clone this repository locally and cd into the *tictactoe* directory.
* Create a new virtual environment::

	$ virtualenv ttt
	$ source ttt/bin/activate
	
* Use ``pip`` to install the necessary requirements::

	(ttt)$ pip install -r requirements.txt
	
* Run syncdb to create the sqlite3 database and setup the django tables::

	(ttt)$ ./manage.py syncdb
	
* Startup the local webserver and navigate to http://localhost:8000 to run the application::

	(ttt)$ ./manage.py runserver
	
	
Tests
------

Unit tests are included for this application and can be run from the command line::

	(ttt)$ ./manage.py test tictactoe.apps.game
	
