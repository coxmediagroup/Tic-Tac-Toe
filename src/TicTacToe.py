#!/usr/bin/env python
# encoding: utf-8
"""
TicTacToe.py

Created by Fredrick Stakem on 2011-01-29.
Copyright (c) 2011 __Stakem Research__. All rights reserved.
"""


class TicTacToe(object):
    """Main class to perform the game TIC TAC TOE.
        
       1)   Algorithm for a win is optimized to reduce the number of compares.
            Each location is givin a unique number that are added together if
            a player occupies that location. The sum of the location numbers
            for each player are compared to the eight known numbers for a win to
            see if the player won. I thought this sounded interesting so I 
            implemented it from this discussion:
            http://www.computing.net/answers/programming/tictactoe-algorithm/3126.html
            
               1  |    2  |    4
             --------------------
               8  |   16  |   32
             --------------------
              64  |  128  |  256 
              
        2)  Positions on the Tic Tac Toe board are defined as follows:
        
              0  |  1  |  2  
            -----------------
              3  |  4  |  5
            -----------------
              6  |  7  |  8
            
    
    """
    
    # Class variables
    __emptyPosition = '-'
    __minPosition = 0
    __maxPosition = 8
    players = ('X', 'O')
    moveResults = ('GAME_OVER_ALREADY', 'INVALID_MOVE', 'INVALID_TURN', 'INVALID_PLAYER', 'WIN', 'CONTINUE')
    __game_location_win_scores = (7, 56, 73, 84, 146, 273, 292, 448)
    
    # Public methods
    #--------------------------------------------------------------------------
    def __init__(self):
        # Initialize all the game state variables
        self.__resetGameState()
        
    def newGame(self):
        self.__resetGameState()
                       
    def nextMove(self, player, position):
        # Check to make sure the move should be allowed
        if self.__winner != None:
            return TicTacToe.moveResults[0]
            
        if self.__last_player_to_move == player:
            return TicTacToe.moveResults[2]
            
        if not self.__checkForValidPlayer(player):
            return TicTacToe.moveResults[3]
            
        if not self.__checkForValidMove(position):
            return TicTacToe.moveResults[1]
        
        # Update the game state
        self.__updateGameState(player, position)
        
        # Check for a win    
        if self.__checkForWin(player):
            return TicTacToe.moveResults[4]
            
        return TicTacToe.moveResults[5]
        
    def getCurrentGameState(self):
        return tuple(self.__state)
        
    def getWinner(self):
        return self.__winner

    # Private methods
    #--------------------------------------------------------------------------     
    def __resetGameState(self):
       self.__winner = None
       self.__last_player_to_move = None
       self.__x_location_score = 0
       self.__o_location_score = 0
       self.__state = [ TicTacToe.__emptyPosition, TicTacToe.__emptyPosition, TicTacToe.__emptyPosition,
                        TicTacToe.__emptyPosition, TicTacToe.__emptyPosition, TicTacToe.__emptyPosition,
                        TicTacToe.__emptyPosition, TicTacToe.__emptyPosition, TicTacToe.__emptyPosition ]
                        
    def __updateGameState(self, player, position):
        self.__state[position] = player
        self.__last_player_to_move = player
        
        if player == TicTacToe.players[0]:
            self.__x_location_score += TicTacToe.__game_location_win_scores[position]
        else:
            self.__y_location_score += TicTacToe.__game_location_win_scores[position]
            
    def __checkForValidPlayer(self, player):
        if player == TicTacToe.players[0] or player == TicTacToe.players[1]:
            return True
            
        return False
                        
    def __checkForValidMove(self, position):
        if self.__state[position] == TicTacToe.__emptyPosition and \
           position >= TicTacToe.__minPosition and \
           position <= TicTacToe.__maxPosition:
            return True
            
        return False
                        
    def __checkForWin(self, player):
        location_score = 0
        if player == TicTacToe.players[0]:
            location_score = self.__x_location_score
        else:
            location_score = self.__y_location_score
            
        for score in TicTacToe.__game_location_win_scores:
            if location_score == score:
                self.__winner = player
                return True
                
        return False



if __name__ == '__main__':
    # Simple test of the class
	game = TicTacToe()
	
	# Move 1
	player = TicTacToe.players[0]
	position = 0
	state = game.nextMove(player, position)
	print TicTacToe.players[0] + " on " + str(position)
	print state + "\n"

