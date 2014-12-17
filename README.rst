Tic-Tac-Toe example app
=======================

To run this app,

  * Ensure you have `django` in your python installation:

      $ pip install django

  * Enter the project and attempt tests:

      $ cd django_tictactoe
      $ python manage.py test

  * Migrate the database, creating a new SQLite file.

      $ python manage.py migrate

  * Run the development server on http://localhost:8000/

      $ python manage.py runserver

There are two user interfaces:

  * Form/POST based UI: http://localhost:8000/

  * Angular single-page UI:  http://localhost:8000/static/single_page.html

  
