'''
Created on Jan 29, 2011

@author: Krzysztof Tarnowski
'''

from engine import NegamaxEngine

class Game(object):
    
    P1 = -1
    P2 = 1
    
    def __init__(self, engine=NegamaxEngine()):
        self._engine = engine
        self._board = [[0]*3]*3
        
    def start(self):
        pass
    
    def play(self, move):
        if move == None:
            move = self._engine.next_move(self._board)
        
        #TODO: Update state
    
    def is_over(self):
        pass
    
    def is_draw(self):
        pass
    
    def has_cross_won(self):
        pass
    
    def get_turn(self):
        pass