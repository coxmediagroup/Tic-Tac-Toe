'''
Created on Jan 29, 2011

@author: Krzysztof Tarnowski
'''

import numpy

import engine

class Game(object):
    
    def __init__(self, engine=engine.NegamaxEngine()):
        self._engine = engine
        self.board = numpy.zeros((3, 3), dtype=numpy.int16)
        self.player = engine.P1
        
    def start(self):
        pass
    
    def play(self, move=None):
        if move == None:
            move = self._engine.next_move(self.board, self.player)
        
        #TODO: Update state
    
    def is_over(self):
        pass
    
    def is_draw(self):
        pass
    
    def has_cross_won(self):
        pass
    
    def get_current_player(self):
        pass