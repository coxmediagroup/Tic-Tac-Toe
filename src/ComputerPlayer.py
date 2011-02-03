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
        
        # TODO => Either add opponents move to state here or in the functions        
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
        open_positions = self.__findOpenPositions()

        if len(open_positions) == 1:
            new_state = copy.deepcopy(current_state)
            next_position = open_positions.pop()
            new_state[next_position] = player
            if ( self.__player == 'x' and self.__isWinner('x') == True ) or \
               ( self.__player == 'o' and self.__isWinner('o') == True ):
                return [ Node(next_position, new_state, 1) ]
            elif ( self.__opponent == 'x' and self.__isWinner('x') == True ) or \
                 ( self.__opponent == 'o' and self.__isWinner('o') == True ):
                return [ Node(next_position, new_state, 1) ]
         
            return [ Node(next_position, new_state, 0) ]

        nodes = []
        for next_position in open_positions:
            new_state = copy.deepcopy(current_state)
            new_state[next_position] = player
            score = 0
            if ( self.__player == 'x' and self.__isWinner('x') == True ) or \
               ( self.__player == 'o' and self.__isWinner('o') == True ):
                score = 1
            elif ( self.__opponent == 'x' and self.__isWinner('x') == True ) or \
                 ( self.__opponent == 'o' and self.__isWinner('o') == True ):
                score = -1
            links = []
            if score == 0:
                # Not sure if you should min or max the links score???
                score = 1
                next_player = None
                if player == 'x':
                    next_player = 'o'
                else:
                    next_player = 'x'
                links = foo(new_state, next_player)
                for link in links:
                    if link.score < score:
                        score = link.score
            
            node = Node(next_position, new_state, score, links)
            nodes.append(node)

        return nodes  
        
    def __findOpenPositions():
        open_positions = []
        for i, state in enumerate(self.__current_state):
            if state == '-':
                open_positions.append(i)
        return open_positions
        
    def __isWinner(self, player):
        pass
        
    def __updateSolutionGraph(self):
        pass


if __name__ == '__main__':
    # Simple test of the class
	player = ComputerPlayer(TicTacToe.players[0])

