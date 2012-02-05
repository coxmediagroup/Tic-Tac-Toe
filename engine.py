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
        returnself.value
        
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
        WIN = 4
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
            
        # semi-apply the move
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

        # undo the semi-apply
        #b[move] = str(move + 1)
        
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
        for move in self.getValidMoves():
            rating = self.__rateMove(move)
            move_node = TTTMoveNode(move, rating)
 
            if rating > 0:
                # Can immediately win, don't apply it and don't recurse. Also,
                # if this is a player win, penalize the weight to push it down
                # the list of potential moves.
                if self.moves % 2 == 0:
                    move_node.weight = -1
                    
                self.applyMove(move)
                move_node = self.__getMoveTree(move_node)
                self.__backOutMove(move)
                parent_node.addChild(move_node)

            else:
                # low-value or blocking move, doesn't mean end-game so apply it
                # and recurse, then back it out for the next potential move
                try:
                    self.applyMove(move)
                    move_node = self.__getMoveTree(move_node)

                except TTTEndGame:
                    # means stalemate, stop recursing
                    pass
                    
                parent_node.addChild(move_node)
                self.__backOutMove(move)
        
        return parent_node
        
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
        
        moves = []
        valid_moves = self.getValidMoves()
        
        if len(valid_moves) == 0:
            # no more moves, stalemate
            raise TTTEndGame('Stalemate!')
            
        for i in valid_moves:
            rating = self.__rateMove(i)
            move_node = TTTMoveNode(i, rating)
            
            if rating > 0:
                # can immediately block; take either one
                return i

            else:
                # low-value move, doesn't mean end-game so apply it
                # and recurse, then back it out for the next potential move
                try:
                    self.applyMove(i)
                    move_node = self.__getMoveTree(move_node)

                except TTTEndGame:
                    # means stalemate, stop recursing
                    pass
                    
                self.__backOutMove(i)
            
            moves.append(move_node)
            
        # sort ascending by weight and return the heaviest one
        sorted(moves, key=lambda node: node.weight)

        return moves[-1].move

# Tracks potential moves, their child moves, and their weights. An optimal
# move is indicated by the path with the highest weight.
class TTTMoveNode:
    def __init__(self, move, weight):
        self.children = []
        self.move = move
        self.weight = weight
        
    def addChild(self, child_node):
        self.children.append(child_node)
        
    # Calculates the current node's weight based on the child with the highest
    # weight after going into each child and calculating their weight but only
    # for the CPU player.
    def calculateWeight(self):
        if len(self.children) > 0:
            for child in self.children:
                child.calculateWeight()
                self.weight += child.weight
    
        return
        
    def __str__(self):
        return 'Move %s, weight %s' % (self.move, self.weight)
