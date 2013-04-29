from django.db import models

# Create your models here.

"""
What makes a move valuable in Tic-Tac-Toe?

- Making a winning move.
- Blocking an opponent from winning.
- Putting a second piece on a win line.
- Preventing an opponent from putting a 2nd piece on a win line.

I wonder if it is possible to assign a numeric value to each of these
conditions as use an simple algorithm to decide which move to make in light
of these.

Here's the basic flow:

1. User clicks a canvas element on the game page.
2. jQuery submits a .get request to Django with the id of the canvas element
clicked by the user.
3. Django records the players move, calculates the response, saves both into
the database/session and send a JSON response to browser which includes the
game status (Keep Going, Game Over, etc.)
4. jQuery parses the JSON response to update the game board with Django's move
and any other necessary changes (like a game over message).

"""