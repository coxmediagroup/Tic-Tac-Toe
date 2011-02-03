#!/usr/bin/env python
# encoding: utf-8
"""
Node.py

Created by Fredrick Stakem on 2011-01-30.
Copyright (c) 2011 __Stakem Research__. All rights reserved.
"""


class Node(object):
    """Node data structure be be used in a graph of the solution for the minimax algorithm.
    """
    
    # Class variables
 
    # Public methods
    #--------------------------------------------------------------------------   
    def __init__(self, current_move=0, game_state=[], score=0, links=[]):
        self.current_move = current_move
        self.game_state = game_state
        self.score = score
        self.links = links
        
    # Private methods
    #--------------------------------------------------------------------------

if __name__ == '__main__':
    node = Node()

