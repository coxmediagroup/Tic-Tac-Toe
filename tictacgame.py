""" A tic-tac-toe game that will only tie or win 
"""
import sys

class PositionAlreadyTakenError(Exception):
     pass

class Board(object):
     """A tic tac toe board"""

     wins = ((0, 1, 2), # rows
             (3, 4, 5),
             (6, 7, 8),
             (0, 3, 6), # columns
             (1, 4, 7),
             (2, 5, 8),
             (0, 4, 8), # diagonals
             (2, 4, 6))

     def __init__(self, *args, **kwargs):
         self.tttboard = [None, None, None,
                          None, None, None,
                          None, None, None]

     def select_position(self, position, player):
         """Sets a position on the board as owned by a player"""

         if self.tttboard[position] is not None:
             raise PositionAlreadyTakenError()

         self.tttboard[position] = player.board_value

     def check_for_win(self, player):
         """Check the board to see if the player has won"""
         winner = False
         for group in Board.wins:
             if self.tttboard[group[0]] == player.board_value \
                     and self.tttboard[group[1]] == player.board_value \
                     and self.tttboard[group[2]] == player.board_value:
                 winner = True
                 break

         return winner

class Player(object):
     """A tic tact toe player"""

     def __init__(self, board_value, *args, **kwargs):
         """
         board_value should be a single character to display such as X or O.
         """

         # the value which will represent the player behind the scenes
         self.board_value = board_value
         self.turn_count = 0

class AIPlayer(Player):
     """An AI tic tac toe player"""

     # These are the positions to target in order
     # after the first turn and any checks for wins/blocks
     # Each list index aligns with the corresponding board position
     STRATEGIES = [(4, 8, 2),
                   (4, 8, 6, 2, 0),
                   (4, 6, 0),
                   (4, 0, 2, 6, 8),
                   None, # should not happen, we ALWAYS get this first
                   (4, 0, 2, 6, 8),
                   (4, 2, 8),
                   (4, 0, 2, 6, 8),
                   (4, 0, 6)]

     def __init__(self, board_value, *args, **kwargs):
         super(AIPlayer, self).__init__(board_value, *args, **kwargs)
         self.strategy = None

     def look_for_win(self, board, player=None):
         """Find a space which allows a win for the given player"""

         win_spot = None
         if player is None:
             player = self
             
         for group in board.wins:
             # creates a list of just the elements of the board which are
             # part of a specific win group and and not already owned by the player
             # and creates a list of tuples of the element and its value.
             not_mine = [(i, val) for i, val in enumerate(board.tttboard)
                         if i in group
                         and val != player.board_value]

             # If there's only one not owned by the ai player and not owned by
             # the other player then select it and we've won
             if len(not_mine) == 1 and not_mine[0][1] is None:
                 # Maybe this should return the selection rather than
                 # modifying the board in here.  Decide later.
                 win_spot = not_mine[0][0]
                 break

         return win_spot

     def pick_open_position(self, board):
         """
         Select any open spot on the board.

         This is a fallback to be used when there are no wins or win blockers.
         """

         open_positions = [i for i, value in enumerate(board.tttboard) if value is None]

         # default no priority position then see if there's a position open
         # which fits the chosen strategy
         selected_position = open_positions[0]

         for position in self.strategy:
             if position in open_positions:
                 selected_position = position
                 break

         return selected_position
         

     def take_turn(self, board, other_player):
         """Implement the logic for a single turn of the AI player"""

         # Always pick the middle box on the first round
         position = 4 if self.turn_count == 0 else None

         if self.turn_count == 1:
             # On the second turn, after the human player has picked
             # their first spot so we can determine our strategy
             assert other_player.board_value in board.tttboard
             player2_position = board.tttboard.index(other_player.board_value)
             self.strategy = AIPlayer.STRATEGIES[player2_position]

         if position is None:
             position = self.look_for_win(board)

         if position is None:
             position = self.look_for_win(board, other_player)

         if position is None:
             position = self.pick_open_position(board)

         self.turn_count += 1
         return position
         
def draw(board):
     """Draw the game board on screen"""
     # ANSI code to clear the screen
     print chr(27) + "[2J"
     for position, value in enumerate(board.tttboard):
         if value is None:
             sys.stdout.write(str(position))
         else:
             sys.stdout.write(str(value))

         if (position + 1) % 3 != 0:
             sys.stdout.write('|')
         else:
             print ''

         if position == 2 or position == 5:
             print '-' * 5
         
         
