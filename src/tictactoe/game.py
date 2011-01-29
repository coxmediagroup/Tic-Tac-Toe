'''
Created on Jan 29, 2011

@author: Krzysztof Tarnowski
'''

from engine import NegamaxEngine

class Game(object):
    
    def __init__(self, engine=NegamaxEngine()):
        self._engine = engine
        
    def start(self):
        pass
    
    def is_over(self):
        pass