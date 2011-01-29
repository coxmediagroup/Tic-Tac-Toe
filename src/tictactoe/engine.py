'''
Created on Jan 29, 2011

@author: Krzysztof Tarnowski
'''

import numpy

P1 = 1
P2 = -1
EMPTY = 0

NOT_STARTED = -2
IN_PROGRESS = 2
P1_WON = 1
P2_WON = -1
DRAW = 0

class Engine(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
    def next_move(self, board, player):
        ''' doc '''
        pass
    
    def get_state(self, board):
        pass
    
    def change_player(self, player):
        return (player == P1) and P2 or P1

    def get_legal_moves(self, board):
        return [(i, j) for i in xrange(0, 3) for j in xrange(0, 3) 
                if board[i, j] == EMPTY]

class NegamaxEngine(Engine):
    '''
    classdocs
    '''
    
    #Can be computed with 2**to_flat_index((i, j)) as well
    _COMP_MATRIX = numpy.array([
                                    [1, 2, 4],
                                    [8, 16, 32],
                                    [64, 128, 256],
                                ])
    
    _WIN_VALUES = (7, 56, 73, 84, 146, 273, 292, 448)
    
    _TOTAL = 511
    
    def __init__(self, max_depth=float('Infinity')):
        Engine.__init__(self)
        self.max_depth = max_depth
        self.move = None
        
    def next_move(self, board, player):
        # P1 = 1, P2 = -1
        self._negamax(board, 0, player, 1)
        
        return self.move
    
    def get_state(self, board):
        #TODO: Something faster; possibly use Magic Square
        total = 0 
        scores = { P1: 0, P2: 0 }
        
        for i in xrange(0, 3):
            for j in xrange(0, 3):
                if board[i, j] != EMPTY:
                    value = NegamaxEngine._COMP_MATRIX[i, j]
                    total += value
                    scores[board[i, j]] += value
                    
        if total ==  NegamaxEngine._TOTAL:
            return DRAW
        
        for win_value in NegamaxEngine._WIN_VALUES:
            if (scores[P1] & win_value) == win_value:
                return P1_WON
            if (scores[P2] & win_value) == win_value:
                return P2_WON
            
        return IN_PROGRESS
        
    def _negamax(self, board, depth, player, color):
        state = self.get_state(board)
        if state != IN_PROGRESS or depth > self.max_depth:
            return color*self._evaluate_board(board, state)
        
        maximum = float('-Infinity')
        
        for move in self.get_legal_moves(board):
            next_board = board.copy()
            next_board[move[0], move[1]] = player
            
            x = -self._negamax(next_board, depth + 1, self.change_player(player), -1*color)
            
            if x > maximum:
                maximum = x
                self.move = move
                
        return maximum
    
    def _evaluate_board(self, board, state):
        if state == P1_WON or state == P2_WON: return 8
        if state == DRAW: return 4
        
        return 1