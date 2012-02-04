#!/usr/bin/python
# Bernhardt, Russell
# russell.bernhardt@gmail.com
""" This module contains all the core functions and objects for game mechanics.
"""

""" Defines a custom exception for easy differentiation between a game error
and a system error.
"""
class TTTError(Exception):

    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)
        
""" Defines a custom exception for indicating a winner... which should never
happen...
"""
class TTTEndGame(Exception):
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)
        
""" The bread n' butter of the whole game. Holdes everything together in a
tight little package, completely separate from the UI.
"""
class TTTEngine(object):
    def __init__(self):
        # the board consists of a nine-element mutable list
        self.board = [ '1', '2', '3', '4', '5', '6', '7', '8', '9' ]
        self.move = 0 # tracks the current move number
        
    """ Check to see if anyone has won, and if so raise the TTTEndGame
    exception. If a stalemate has occured, raises the TTTStalemate exception.
    """        
    def checkState(self):
        pass
        
    # Given a digit that represents the slot to move into
    def applyMove(self, move):
        pass
        
    # Returns a list of valid moves given the current game state
    def getValidMoves(self):
        pass
        
    # Give a list of valid moves, returns the most damaging one based on the
    # current game state
    def getBestMove(self, moves):
        pass
        
