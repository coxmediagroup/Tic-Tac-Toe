"""
Functions and classes for playing the game. The UI classes can be found in
run.py
"""
import re


class TicTacToeBoard(object):
    """
    Primary class for tracking and playing the game.  
    
    Each of the nine squares on the board is represented by a number, like so:
                    ___________
                   | 8 | 7 | 6 |
                    -----------
                   | 1 | 0 | 5 |
                    -----------
                   | 2 | 3 | 4 |
                    -----------
    
    These numbers directly correspond to positions in the binary representation
    of the board. An empty board would be represented in binary as:
    
             [8]  [7]  [6]  [5]  [4]  [3]  [2]  [1]  [0]
             0 0  0 0  0 0  0 0  0 0  0 0  0 0  0 0  0 0
             
    The first bit of the two-bit representation of a square indicates whether
    or not the position is filled. The second bit represents either an 'X' (1)
    or an 'O' (0). For example:
                    ___________
                   | X |   |   |
                    -----------
                   |   | O | O |
                    -----------
                   |   | X |   |
                    -----------
    
    This board can be represented in binary as:
       
             [8]  [7]  [6]  [5]  [4]  [3]  [2]  [1]  [0]
             1 1  0 0  0 0  1 0  0 0  1 1  0 0  0 0  1 0
             
    This value is stored as a hex value to make it shorter, so this board would 
    be represented as 0x3080c2.
    """
    def __init__(self):
        super(TicTacToeBoard, self).__init__()
        self.board = 0x00000
        self.turn = 0
        self.player_wins = 0
        self.player_losses = 0
        self.ties = 0