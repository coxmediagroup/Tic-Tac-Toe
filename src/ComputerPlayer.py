#!/usr/bin/env python
# encoding: utf-8
"""
ComputerPlayer.py

Created by Fredrick Stakem on 2011-01-29.
Copyright (c) 2011 __Stakem Research__. All rights reserved.
"""

import TicTacToe as TicTacToe

class ComputerPlayer(object):
    """
    
    
    
    """
 
    # Public methods
    #--------------------------------------------------------------------------   
    def __init__(self, player):
        self.__resetState(player)
        
    def newGame(self, player):
        self.__resetState(player)
        
    def getNextMove(self, game_state):
        move = self.calculateMove(game_state)
        if move == -1:
            return move
        elif move == 1:
            return self.__findFirstMove(game_state)
        else:
            return self.__findOptimalMove(game_state, move)
        
    # Private methods
    #--------------------------------------------------------------------------
    def __resetState(self, player):
        # Game solutions
        self.__player = self.__checkForValidPlayer(player)
        self.__solutions = None
        
    def __checkForValidPlayer(self, player):
        if player == TicTacToe.players[0] or player == TicTacToe.players[1]:
            return player

        return TicTacToe.players[0]
        
    def __calculateMove(self, game_state):
        pass
                
    def __calculateSolutionGraph(self):
        pass
        
    def __getOtherPlayersInitialMove(self):
        pass
        
    def __findFirstMove(self, game_state):
        pass
        
    def __findOptimalMove(self, game_state):
        if self.__solutions == None:
            self.__calculateSolutionGraph()


if __name__ == '__main__':
    #main()
    pass

