'''
Created on Jan 29, 2011

@author: Krzysztof Tarnowski
'''

import numpy

import engine

class Game(object):
    
    def __init__(self, game_engine=engine.RulesBasedEngine()):
        self._engine = game_engine
        self._state = engine.NOT_STARTED
        self.board = numpy.zeros((3, 3), dtype=numpy.int16)
        self.player = engine.P1
        
    def start(self):
        self._state = engine.IN_PROGRESS
    
    def play(self, move=None, game_engine=None):
        game_engine = game_engine and game_engine or self._engine
        
        if move == None:
            move = game_engine.next_move(self.board, self.player)
        
        self.board[move[0], move[1]] = self.player
        self.player = game_engine.change_player(self.player)
        self._state = game_engine.get_state(self.board)
    
    def is_over(self):
        return self._state != engine.NOT_STARTED and self._state != engine.IN_PROGRESS
    
    def is_draw(self):
        return self._state == engine.DRAW
    
    def has_cross_won(self):
        return self._state == engine.P1_WON
    
    def is_valid(self, move):
        pass