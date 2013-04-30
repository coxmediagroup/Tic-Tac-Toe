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
import random

class GameEngine(object):
    GAME_WINNING_COMBINATIONS = (
        (1, 2, 3), (4, 5, 6), (7, 8, 9), # Rows Wins
        (1, 4, 7), (2, 5, 8), (3, 6, 9), # Column Wins
        (1, 5, 9), (3, 5, 7))               # Diagonal Wins

    GAME_SQUARES = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def __init__(self, players_move_history, computers_move_history):
        self.players_move_history = players_move_history
        self.computers_move_history = computers_move_history

        self.open_squares = set(
            self.computers_move_history +
            self.players_move_history).symmetric_difference(
                GameEngine.GAME_SQUARES)

    def next_computer_move(self):
        """
        Determine the next move for the computer to make in order to bring
        complete destruction and utter humiliation to the player.

        """
        for move_list in (self.computers_move_history,
                          self.players_move_history):

            next_move = self.check_for_winning_move(move_list)
            if next_move:
                return next_move

        return self.random_move()

    def check_for_winning_move(self, move_history_to_evaluate):
        """
        Determine if a winning move is available and if so return it.

        Compare a given move history to all possible game winning
        combinations.  If a combination is found where 2 out of 3
        squares have been selected, see if the 3rd is still available.

        If it is, return it.

        """
        for winning_combination in GameEngine.GAME_WINNING_COMBINATIONS:

            # Evaluate move history against current winning combination.
            moves_already_selected = set(
                move_history_to_evaluate).intersection(winning_combination)

            # If two elements are in common, identify the last element.
            if moves_already_selected.__len__() == 2:
                next_move = moves_already_selected.symmetric_difference(
                    winning_combination).pop()

                # See if last element is selectable. If so, return it.
                if next_move in self.open_squares:
                    return next_move

    def is_square_open(self, square_id):
        """
        Determine if a given square is still available for selection.

        """
        # Determine which spots are still open.
        open_squares = set(
            self.computers_move_history +
            self.players_move_history).symmetric_difference(
                GameEngine.GAME_SQUARES)

        if square_id in open_squares:
            return True

    def random_move(self):
        """



        """
        list_of_open_squares = list(self.open_squares).remove([1,2,3])
        return random.choice(list_of_open_squares)