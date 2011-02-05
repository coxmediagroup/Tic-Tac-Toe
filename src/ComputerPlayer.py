#!/usr/bin/env python
# encoding: utf-8
"""
ComputerPlayer.py

Created by Fredrick Stakem on 2011-01-29.
Copyright (c) 2011 __Stakem Research__. All rights reserved.
"""

from TicTacToe import *
from Node import *
import random


class ComputerPlayer(object):
    """Computer AI to play Tic Tac Toe game.
    
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
    __min_position = 0
    __max_position = 8
    __all_positions = range(__min_position, __max_position)
    __game_location_values = (1, 2, 4, 8, 16, 32, 64, 128, 256)
    __game_location_win_scores = (7, 56, 73, 84, 146, 273, 292, 448)
 
    # Public methods
    #--------------------------------------------------------------------------   
    def __init__(self, player):
        self.__resetState(player)
        
    def newGame(self, player):
        self.__resetState(player)
        
    def getNextMove(self, opponents_move):
        next_move = -1
        if len(self.__current_state) > 7 or opponents_move < 0 or opponents_move > 8:
            return next_move
              
        if len(self.__current_state) == 0:
            next_move = self.__findFirstMove(opponents_move)
        else:
            next_move = self.__findOptimalMove(opponents_move)
           
        self.__current_state[next_move] = self.__player
        return next_move
        
    # Private methods
    #--------------------------------------------------------------------------
    def __resetState(self, player):
        # Game solutions
        self.__player, self.__opponent = self.__checkForValidPlayer(player)
        self.__solutions = None
        self.__current_state = [ TicTacToe.__empty_position, TicTacToe.__empty_position, TicTacToe.__empty_position,
                                 TicTacToe.__empty_position, TicTacToe.__empty_position, TicTacToe.__empty_position,
                                 TicTacToe.__empty_position, TicTacToe.__empty_position, TicTacToe.__empty_position ]
        
    def __checkForValidPlayer(self, player):
        if player == TicTacToe.players[0]:
            return [TicTacToe.players[0], TicTacToe.players[1]]
        elif player == TicTacToe.players[1]:
            return [TicTacToe.players[1], TicTacToe.players[0]]

        return TicTacToe.players[0]
                        
    def __findFirstMove(self, opponents_move):
        if opponents_move == -1:
            return random.randrange(0,9,2)
        else:
            self.__current_state[opponents_move] = self.__opponent
            
            if opponents_move == 4:
                return random.choice([0, 2, 6, 8])
            elif opponents_move == 0 or opponents_move == 2 or \
                 opponents_move == 6 or opponents_move == 8:
                return 4
            else:
                return random.choice([0, 2, 4, 6, 8])
        
    def __findOptimalMove(self, opponents_move):
        self.__current_state[opponents_move] = self.__opponent
        
        if self.__solutions == None:
            self.__calculateSolutionGraph()
        else:
            self.__updateSolutionGraph()
            
        # TODO -> add simple code to pick the next move from the graph
        
        return 1
            
    def __calculateSolutionGraph(self):
        possible_moves = set(ComputerPlayer.__all_positions) - set(self.__self.__previous_moves) 
       
    def __generateNodes(self, current_state, player):
        open_positions = self.__findOpenPositions(current_state)

        if len(open_positions) == 1:
            new_state = copy.deepcopy(current_state)
            next_position = open_positions.pop()
            new_state[next_position] = player
            return [ Node(next_position, new_state, self.__calculateGameScore(self.__player, new_state)) ]

        nodes = []
        for next_position in open_positions:
            new_state = copy.deepcopy(current_state)
            new_state[next_position] = player
            score = self.__calculateGameScore(self.__player, new_state)
            links = []
            if score == 0:
                next_player = self.__getOtherPlayer(player)
                links = foo(new_state, next_player)
                score = self.__findBestScore(links)
                
            node = Node(next_position, new_state, score, links)
            nodes.append(node)

        return nodes  
        
    def __findOpenPositions(self, current_state):
        open_positions = []
        for i, state in enumerate(current_state):
            if state == TicTacToe.empty_position:
                open_positions.append(i)
        return open_positions
        
    def __calculateGameScore(self, player, game_state):
        if ( player == TicTacToe.players[0] and self.__isWinner(TicTacToe.players[0], game_state) == True ) or \
           ( player == TicTacToe.players[1] and self.__isWinner(TicTacToe.players[1], game_state) == True ):
            return 1
        elif ( player == TicTacToe.players[1] and self.__isWinner(TicTacToe.players[0], game_state) == True ) or \
             ( player == TicTacToe.players[0] and self.__isWinner(TicTacToe.players[1], game_state) == True ):
            return -1
            
        return 0
        
    def __isWinner(self, player, game_state):
        score = 0
        for i, state in enumerate(game_state):
            if state == player:
                score += TicTacToe.game_location_values[i]
                
        if score in TicTacToe.game_location_win_scores:
            return True
            
        return False
        
    def __getOtherPLayer(self, player):
        if player == TicTacToe.players[0]:
            return TicTacToe.players[1]
        
        return TicTacToe.players[0]
        
    def __findBestScore(self, links):
        # TODO => redo this
        score = 0
        for node in links:
            if node.score < score:
                score = node.score
                
        return score
                
    def __updateSolutionGraph(self):
        pass


if __name__ == '__main__':
    # Simple test of the class
	player = ComputerPlayer(TicTacToe.players[0])

