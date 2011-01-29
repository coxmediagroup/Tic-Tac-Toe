'''
Created on Jan 29, 2011

@author: Krzysztof Tarnowski
'''

import copy

P1 = -1
P2 = 1

IN_PROGRESS = 0
P1_WON = 1
P2_WON = -1
DRAW = 2

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
    
    def _change_player(self, player):
        return player == P1 and P1 or P2

class NegamaxEngine(Engine):
    '''
    classdocs
    '''
    
    def __init__(self, max_depth=float('Infinity')):
        Engine.__init__(self)
        self.max_depth = max_depth
        self.move = None
        
    def next_move(self, board, player):
        self._negamax(board, 0, player)
        
        return self.move
    
    def get_state(self, board):
        pass
        
    def _negamax(self, board, depth, player):
        state = self.get_state(board) 
        if state != IN_PROGRESS or depth > self.max_depth:
            return player*self._evaluate_board(board, player)
        
        maximum = float('-Infinity')
        
        for move in self._get_legal_moves(board):
            next_board = copy.deepcopy(board)
            next_board[move[0]][move[1]] = player
            
            x = -self._negamax(next_board, depth + 1, self._change_player(player))
            
            if x > maximum:
                maximum = x
                self.move = move
                
        return maximum
    
    def _evaluate_board(self, board, player):
        pass    
        
    def _get_legal_moves(self, board):
        pass