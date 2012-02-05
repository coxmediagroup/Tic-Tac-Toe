#!/usr/bin/python
# Bernhardt, Russell
# russell.bernhardt@gmail.com

""" This module contains all the core functions and objects for game mechanics.
"""

""" Defines a custom exception for easy differentiation between a game error
and a system error. Game errors can be caught and handled by the UI. System
errors will be generic Exceptions.
"""
class TTTError(Exception):

    def __init__(self, value):
        self.value = str(value)
        
    def __str__(self):
        return self.value
        
""" Defines a custom exception for indicating a winner.
"""
class TTTEndGame(Exception):
    def __init__(self, value):
        self.value = str(value)
        
    def __str__(self):
        return self.value
        
""" The bread n' butter of the whole game. Holdes everything together in a
tight little package, completely separate from the UI.
"""
class TTTEngine:
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
        
    # given a digit that represents the slot to move into
    def applyMove(self, move):
        # check that move is valid before applying it, raising a TTTError if not
        if not move in range(0,9) or not self.board[ move ].isdigit():
            # the specified slot is taken, so invalid move
            raise TTTError('Please choose an open position.')
            
        if self.moves % 2 == 0:
            # this is X's turn
            self.board[ move ] = 'X'
        else:
            # this is O's turn
            self.board[ move ] = 'O'
            
        self.moves += 1
        
        self.checkState()
        
    # returns a list of any open space on the board
    def getValidMoves(self):
        avail_moves = []
        for i in range(0,9):
            if self.board[i].isdigit():
                avail_moves.append(i)
        
        return avail_moves
        
    # Internal function to rate the given move with the current board state.
    # Returns 2 for a winning move, 1 for a blocking move, else 0 for other.
    def __rateMove(self, move):
        WIN = 5 # super-prioritize winning; AI would often prefer to block
        BLOCK = 1
        OTHER = 0
        
        corners = (0, 2, 6, 8)
        middle = 4
        player = 'X'
        # copy the board
        b = self.board[:]

        if not move in self.getValidMoves():
            raise Exception('A non-available move was given.')
        
        # at this point, the move in question has not yet been played
        if self.moves % 2 != 0:
            player = 'O'
            
        # fake-apply the move the the board copy
        b[move] = player

       # check for win
        if ( move in (0, 1, 2) ) and ( b[0] == b[1] == b[2] ) or \
          ( move in (3, 4, 5) ) and ( b[3] == b[4] == b[5] ) or \
          ( move in (6, 7, 8) ) and ( b[6] == b[7] == b[8] ) or \
          ( move in (0, 3, 6) ) and ( b[0] == b[3] == b[6] ) or \
          ( move in (1, 4, 7) ) and ( b[1] == b[4] == b[7] ) or \
          ( move in (2, 5, 8) ) and ( b[2] == b[5] == b[8] ):
            return WIN
            
        # check diagonals is move is on a corner or in middle
        if move in corners or move == middle:
            if ( move in (0, 4, 8) ) and ( b[0] == b[4] == b[8] ) or \
              ( move in (2, 4, 6) ) and ( b[2] == b[4] == b[6] ):
                return WIN
   
        # look for a block; same combos as win, but with one player off. Use
        # math and numbers.
        for i in range(0, 9):
            if b[i] == 'X':
                b[i] = 2
            elif b[i] == 'O':
                b[i] = 1
            else:
                b[i] = 0
        
        # the total X needs to block is 4, O needs 5 per row.
        tot = 4
        if player == 'O':
            tot = 5
            
        # a block would be 2 + 2 + 1 = 5 if player move or
        # 1 + 1 + 2 = 4 if CPU move
        if ( move in (0, 1, 2) ) and ( b[0] + b[1] + b[2] == tot ) or \
          ( move in (3, 4, 5) ) and ( b[3] + b[4] + b[5] == tot ) or \
          ( move in (6, 7, 8) ) and ( b[6] + b[7] + b[8] == tot ) or \
          ( move in (0, 3, 6) ) and ( b[0] + b[3] + b[6] == tot ) or \
          ( move in (1, 4, 7) ) and ( b[1] + b[4] + b[7] == tot ) or \
          ( move in (2, 5, 8) ) and ( b[2] + b[5] + b[8] == tot ):
            return BLOCK

         
        if move in corners or move == middle:
            if ( move in (0, 4, 8) ) and ( b[0] + b[4] + b[8] == tot ) or \
              ( move in (2, 4, 6) ) and ( b[2] + b[4] + b[6] == tot):
                return BLOCK
            
        # by now the move has become unvaluable
        return OTHER
        
    # Back out the specified move (reset the space and decrement the moves
    # counter. Move is the actual index in the board list.
    def __backOutMove(self, move):
        if not self.board[move].isalpha():
            raise Exception('Space given is not occupied.')
            
        self.board[move] = str(move + 1)
        self.moves -= 1
        
    # Given a move node and the current game state, generates a weighted move
    # tree for any available moves and appends them to the given move node's
    # children list. Returns the modified move node.
    def __getMoveTree(self, parent_node):
        move_list = self.getValidMoves()
        
        if len(move_list) == 0:
            # no more moves, board is currently full so just return
            return parent_node

        # rate each move and determine the best course of action
        for move in move_list:
            rating = self.__rateMove(move)
            move_node = TTTMoveNode(move, rating)
 
            # On predicted player moves, zero out the weight
            if self.moves % 2 == 0:
                move_node.weight = 0
                
            try:
                self.applyMove(move)
                move_node = self.__getMoveTree(move_node)
                
                if self.moves % 2 != 0:
                    parent_node.weight += rating

            except TTTEndGame:
                pass
                
            self.__backOutMove(move)
            parent_node.addChild(move_node)
        
        return parent_node
        
        
    # Returns True if the specified move occurs on a corner. Used for when a
    # tie occurs between multiple moves. Corners are preferred if nothing else.
    def __isCorner(self, move):
        return move in (0, 2, 6, 8)
    
    # Runs the AI to determine the best next move for the CPU.
    def getBestMove(self):
        # manual override for first move seems to iron out some "stupid"
        # decisions the AI likes to make when it has too many choices or if
        # the game is too vague
        if self.moves == 1:
            if 4 in self.getValidMoves():
                return 4
            
            else:
                return 0
        
        # start the move tree with a root node move of -1
        moves = self.__getMoveTree( TTTMoveNode(-1, 0) )
            
        # sort ascending by weight and return the heaviest one
        moves.children = sorted(moves.children, key=lambda node: -node.weight)
        
        # check for ties, returning a corner if possible
        if len(moves.children) > 1 and \
          moves.children[0].weight == moves.children[1].weight:
            if self.__isCorner(moves.children[0].move):
                return moves.children[0].move
                
            else:
                return moves.children[1].move
                
        else:
            return moves.children[0].move

# Tracks potential moves, their child moves, and their weights. An optimal
# move is indicated by the path with the highest weight.
class TTTMoveNode:
    def __init__(self, move, weight):
        self.children = []
        self.move = move
        self.weight = weight
        
    def addChild(self, child_node):
        self.children.append(child_node)
        
