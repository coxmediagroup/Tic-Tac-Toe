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
class TTTEngine:
    def __init__(self):
        # the board consists of a nine-element mutable list
        self.board = [ '1', '2', '3', '4', '5', '6', '7', '8', '9' ]
        self.moves = 0 # tracks the number of completed moves

        self.AI_DEPTH = 4 # how many moves to look ahead
        self.curr_depth = 0 # tracks the current depth of the AI
        
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
        return 0
        
    # Back out the specified move (reset the space and decrement the moves
    # counter. Move is the actual index in the board list.
    def __backOutMove(self, move):
        self.board[move] = str(move + 1)
        self.moves -= 1
        
    # Given a move node and the current game state, generates a weighted move
    # tree for any available moves and appends them to the given move node's
    # children list. Returns the modified move node.
    def __getMoveTree(self, parent_node):
        if self.curr_depth > self.AI_DEPTH:
            # stop looking ahead and just return
            self.curr_depth -= 1
            return parent_node
            
        self.curr_depth += 1
        move_list = self.getValidMoves()
        
        if len(move_list) == 0:
            # no more moves, board is currently full so just return
            return parent_node

        # rate each move and determine the best course of action
        for move in move_list:
            rating = self.__rateMove(move)
            move_node = TTTMoveNode(move, rating)
            
            if self.moves % 2 == 0:
                # this is a cpu turn, so say so
                move_node.is_cpu = True

            if rating == 2:
                # Can immediately win, don't apply it and don't recurse. Also,
                # if this is a player win, penalize the weight to push it down
                # the list of potential moves.
                if not move_node.is_cpu:
                    move_node.weight = -1
                    
                parent_node.addChild(move_node)
            
            else:
                # low-value or blocking move, doesn't mean end-game so apply it
                # and recurse, then back it out for the next potential move
                self.applyMove(move)
                move_node = self.getMoveTree(move_node)
                parent_node.addChild(move_node)
                self.__backOutMove(move)
        
        return parent_node
        
    # Runs the AI to determine the best next move for the CPU.
    def getBestMove(self):
        moves = []
        for i in self.getValidMoves():
            move_node = self.__getMoveTree( TTTMoveNode(i, 0) )
            move_node.calculateWeight()
            moves.append(move_node)
            
        sorted(moves, key=lambda node: node.weight)
        return moves[0].move

# Tracks potential moves, their child moves, and their weights. An optimal
# move is indicated by the path with the highest weight.
class TTTMoveNode:
    def __init__(self, move, weight):
        self.children = []
        self.move = move
        self.weight = weight
        self.is_cpu = False
        
    def addChild(self, child_node):
        self.children.append(child_node)
        
    # Calculates the current node's weight based on the child with the highest
    # weight after going into each child and calculating their weight but only
    # for the CPU player.
    def calculateWeight(self):
        if len(self.children) > 0:
            for child in self.children:
                child.calculateWeight()
    
            # sort children by weight descending
            sorted( self.children, key=lambda child: child.weight )
        
            # add only the heaviest child to current weight and only if it's the
            # cpu's play
            if self.children[0].is_cpu:
                self.weight += self.children[0].weight
        
        return
