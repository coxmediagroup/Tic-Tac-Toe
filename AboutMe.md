Tic Tac Toe Game Django App

Features:

    1. Tic Tac Toe game where a player plays against the computer
    2. Player Sign Up, Login and Logout
    3. The computer never loses. Implemented using the minimax algorithm (http://en.wikipedia.org/wiki/Minimax)
    4. Game History for each user stored in sqllite3 db (Game time, result and counts)
    5. System highlights the winning combination

Instructions for running this app:
    1. This app was built using the following packages:
        - Python (Version 2.7.2)
        - Django (Version 1.5.2)

    2. I have included the copy of my test db (sqlite3.db) so it should be working automatcally using that. The admin user is janit/janit

    3. Start the server using: python tictactoe/manage.py runserver. Access the game at http://127.0.0.1:8000/

QA:
   QA for this app was done by running a unit test (in core/tests.py) which simulates 1000 games between a human player and the computer and makes sure that the computer never loses. The test takes about 80-180 secs.


