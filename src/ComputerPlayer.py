#!/usr/bin/env python
# encoding: utf-8
"""
ComputerPlayer.py

Created by Fredrick Stakem on 2011-01-29.
Copyright (c) 2011 __Stakem Research__. All rights reserved.
"""

import TicTacToe as TicTacToe

class ComputerPlayer(object):
    """Computer AI to play Tic Tac Toe game.
    
        1)  Positions on the Tic Tac Toe board are defined as follows:
    
              0  |  1  |  2  
            -----------------
              3  |  4  |  5
            -----------------
              6  |  7  |  8    
    """
 
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
                
        if self.__move_count == 0:
            next_move = self.__findFirstMove(last_move)
        else:
            self.__move += 1
            next_move = self.__findOptimalMove(last_move)
            
        self.__move_count += 1
        return next_move
        
    # Private methods
    #--------------------------------------------------------------------------
    def __resetState(self, player):
        # Game solutions
        self.__player = self.__checkForValidPlayer(player)
        self.__solutions = None
        self.__move_count = 0
        
    def __checkForValidPlayer(self, player):
        if player == TicTacToe.players[0] or player == TicTacToe.players[1]:
            return player

        return TicTacToe.players[0]
                        
    def __findFirstMove(self, last_move):
        if last_move == -1:
            pass
        else:
            pass
        
    def __findOptimalMove(self, last_move):
        if self.__solutions == None:
            self.__calculateSolutionGraph()
            
    def __calculateSolutionGraph(self):
        pass


if __name__ == '__main__':
    #main()
    pass

