__author__ = 'henryadam'

import random

class Board(object):
    """a tic tac toe matrix"""
    wins = ((0,1,2), # rows
            (3,4,5),
            (6,7,8),
            (0,3,6), # columns
            (1,4,7),
            (2,5,8),
            (0,4,8), # diagonals
            (2,4,6))

    def __init__(self, *args, **kwargs):
        """
            The board is the passed in board or a blank board since this AI always wins, we will always render
            an initialized board where the computer takes the middle
        """
        self.the_board = kwargs.get('the_board',[None, None, None, None, None, None, None, None, None])


    def draw(self):
        """
            This function will draw a bootstrap html table based on a sequence received in the argument board
            so that a board [0,1,2,3,4,5,6,7,8]
        """
        draw_this = """<div  class="row-fluid">
                <div id="cell_0" class="offset1 span3 well">
                    <h1 class="text-center">%s</h1>
                </div>
                <div id="cell_1" class="span3 well">
                   <h1 class="text-center">%s</h1>
                </div>
                <div id="cell_2" class="span3 well">
                    <h1 class="text-center">%s</h1>
                </div>
            </div>
            <div class="row-fluid">
                <div id="cell_3" class="offset1 span3 well">
                    <h1 class="text-center">%s</h1>
                </div>
                <div id="cell_4" class="span3 well">
                   <h1 class="text-center">%s</h1>
                </div>
                <div id="cell_5" class="span3 well">
                    <h1 class="text-center">%s</h1>
                </div>
            </div>
            <div class="row-fluid">
                <div id="cell_6" class="offset1 span3 well">
                   <h1 class="text-center">%s</h1>
                </div>
                <div id="cell_7" class="span3 well">
                    <h1 class="text-center">%s</h1>
                </div>
                <div id="cell_8" class="span3 well">
                    <h1 class="text-center">%s</h1>
                </div>
            </div>""" % (self.the_board[0],self.the_board[1],self.the_board[2],self.the_board[3],self.the_board[4],self.the_board[5],self.the_board[6],self.the_board[7],self.the_board[8])
        return(draw_this)

class Player(object):
    """A tic tact toe player"""

    def __init__(self, board_value, *args, **kwargs):
        """
        board_value should be a single character to display such as X or O.
        """

        self.board_value = board_value  # the value which will represent the player behind the scenes

class AIPlayer(Player):
    """I am the AI player for this game"""

    def look_for_win(self, board, player=None):
        """Find a space which allows a win for the given player"""
        pass