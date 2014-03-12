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


