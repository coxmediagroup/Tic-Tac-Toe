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
        self.moves = 0 # tracks the number of completed moves
        
    """ Check to see if anyone has won, and if so raise the TTTEndGame
    exception. If a stalemate has occured, raises the TTTStalemate exception.
    """        
    def checkState(self):
        # little shortcut
        b = self.board
        
        # winning combos:
        # 1-2-3 / 4-5-6 / 7-8-9 / 1-5-9 / 3-5-7 / 2-5-8 / 1-4-6 / 3-6-9
        if ( b[0] == b[1] == b[2] ) or ( b[3] == b[4] == b[5] ) or \
          ( b[6] == b[7] == b[8] ) or ( b[0] == b[4] == b[8] ) or \
          ( b[2] == b[4] == b[6] ) or ( b[1] == b[4] == b[7] ) or \
          ( b[0] == b[3]== b[6] ) or ( b[2] == b[5] == b[8] ):
            
            winner = 'You'
            if self.moves % 2 == 0:
                winner = 'I'
    
            raise TTTEndGame('%s won!' % winner)
        
        # no winner, so check for stalemate (all X's and O's)
        elif len( ''.join(b).replace('X','').replace('O','') ) == 0:
            raise TTTEndGame('Stalemate!')
            
        # no else because there was no winner and no stalemate
        
    # Given a digit that represents the slot to move into
    def applyMove(self, move):
        # check that move is valid before applying it, raising a TTTError if not
        if not move in range(1,10) or not self.board[ move - 1 ].isdigit():
            # the specified slot is taken, so invalid move
            raise TTTError('Please choose an open position.')
            
        if self.moves % 2 == 0:
            # this is X's turn
            self.board[ move - 1] = 'X'
        else:
            # this is O's turn
            self.board[ move - 1] = 'O'
            
        self.moves += 1
        
    # Returns a list of valid moves given the current game state; basically
    # any open space
    def getValidMoves(self):
        avail_moves = []
        for i in range(0,9):
            if self.board[i].isdigit():
                avail_moves.append( i + 1 )
        
        return avail_moves
        
    # Give a list of valid moves, returns the most damaging one based on the
    # current game state; all AI logic will go in here.
    def getBestMove(self, moves):
        pass
        
