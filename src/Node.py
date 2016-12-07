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
    def __init__(self, move=0, game_state=[], score=0, links=[]):
        self.move = move
        self.game_state = game_state
        self.score = score
        self.links = links
        
    def __str__(self):
        output = str(self.score) + "\n" + self.__getGameBoard() + "\n"
        for node in self.links:
            output += str(node)
        output += "-----------------\n"
        return output
        
    # Private methods
    #--------------------------------------------------------------------------
    def __getGameBoard(self):
        return " " + str(self.game_state[0]) + " | " + str(self.game_state[1]) + " | " + str(self.game_state[2]) + "\n" + \
               " " + str(self.game_state[3]) + " | " + str(self.game_state[4]) + " | " + str(self.game_state[5]) + "\n" + \
               " " + str(self.game_state[6]) + " | " + str(self.game_state[7]) + " | " + str(self.game_state[8]) + "\n"
       

if __name__ == '__main__':
    node = Node()

