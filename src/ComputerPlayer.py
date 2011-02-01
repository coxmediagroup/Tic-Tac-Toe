#!/usr/bin/env python
# encoding: utf-8
"""
ComputerPlayer.py

Created by Fredrick Stakem on 2011-01-29.
Copyright (c) 2011 __Stakem Research__. All rights reserved.
"""

from TicTacToe import *
import random


class ComputerPlayer(object):
    """Computer AI to play Tic Tac Toe game.
    
        1)  Positions on the Tic Tac Toe board are defined as follows:
    
              0  |  1  |  2  
            -----------------
              3  |  4  |  5
            -----------------
              6  |  7  |  8    
    """
    
    # Class variables
    __min_position = 0
    __max_position = 8
    __all_positions = range(__min_position, __max_position)
 
    # Public methods
    #--------------------------------------------------------------------------   
    def __init__(self, player):
        self.__resetState(player)
        
    def newGame(self, player):
        self.__resetState(player)
        
    def getNextMove(self, last_move):
        next_move = -1
        if self.__move_count > 8 or last_move < 0 or last_move > 8:
            return next_move
                
        if len(self.__previous_moves) == 0:
            next_move = self.__findFirstMove(last_move)
        else:
            next_move = self.__findOptimalMove(last_move)
         
        self.__previous_moves.append(next_move)   
        return next_move
        
    # Private methods
    #--------------------------------------------------------------------------
    def __resetState(self, player):
        # Game solutions
        self.__player = self.__checkForValidPlayer(player)
        self.__solutions = None
        self.__previous_moves = []
        
    def __checkForValidPlayer(self, player):
        if player == TicTacToe.players[0] or player == TicTacToe.players[1]:
            return player

        return TicTacToe.players[0]
                        
    def __findFirstMove(self, last_move):
        move = -1
        if last_move == -1:
            return random.randrange(0,9,2)
        else:
            self.__previous_moves.append(last_move) 
            
            if last_move == 4:
                return random.choice([0, 2, 6, 8])
            elif last_move == 0 or last_move == 2 or \
                 last_move == 6 or last_move == 8:
                return 4
            else:
                return random.choice([0, 2, 4, 6, 8])
        
    def __findOptimalMove(self, last_move):
        self.__previous_moves.append(last_move)
        
        if self.__solutions == None:
            self.__calculateSolutionGraph()
        else:
            self.__updateSolutionGraph()
            
        # TODO -> add simple code to pick the next move from the graph
        
        return 1
            
    def __calculateSolutionGraph(self):
        possible_moves = set(ComputerPlayer.__all_positions) - set(self.__self.__previous_moves) 
            
        
    def __updateSolutionGraph(self):
        pass


if __name__ == '__main__':
    # Simple test of the class
	player = ComputerPlayer(TicTacToe.players[0])

