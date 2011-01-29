'''
Created on Jan 29, 2011

@author: Krzysztof Tarnowski
'''

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
    
    def is_over(self):
        pass

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
        
    def _negamax(self, board, depth, player):
        pass