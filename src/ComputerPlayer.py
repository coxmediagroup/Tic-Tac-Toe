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
import copy


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
    __winning_combinations = ( (0, 1, 2), (3, 4, 5), (6, 7, 8), 
                               (0, 3, 6), (1, 4, 7), (2, 5, 8), 
                               (0, 4, 8), (2, 4, 6) )
    __winning_score = 1000
    __good_score = 100
 
    # Public methods
    #--------------------------------------------------------------------------   
    def __init__(self, player):
        self.__resetState(player)
        
    def newGame(self, player):
        self.__resetState(player)
        
    def getNextMove(self, opponents_move):
        next_move = -1
        open_positions = self.__findOpenPositions(self.__current_state)
        
        # Error no positions open or incorrect move
        if len(open_positions) == 0 or opponents_move < 0 or opponents_move > 8:
            return next_move
        
        # First move      
        if len(open_positions) >= 8:
            next_move = self.__findFirstMove(opponents_move)
        # Second move
        elif if len(open_positions) >= 6:
            next_move = self.__findSecondMove(opponents_move)
        # Subsequent moves
        else:
            next_move = self.__findOptimalMove(opponents_move)
             
        return next_move
        
    # Private methods
    #--------------------------------------------------------------------------
    def __resetState(self, player):
        # Game solutions
        self.__player, self.__opponent = self.__checkForValidPlayer(player)
        self.__solutions = None
        self.__current_state = [ TicTacToe.empty_position, TicTacToe.empty_position, TicTacToe.empty_position,
                                 TicTacToe.empty_position, TicTacToe.empty_position, TicTacToe.empty_position,
                                 TicTacToe.empty_position, TicTacToe.empty_position, TicTacToe.empty_position ]
        
    def __checkForValidPlayer(self, player):
        if player == TicTacToe.players[0]:
            return [TicTacToe.players[0], TicTacToe.players[1]]
        elif player == TicTacToe.players[1]:
            return [TicTacToe.players[1], TicTacToe.players[0]]

        return TicTacToe.players[0]
                        
    def __findFirstMove(self, opponents_move):
        next_move = -1
        
        # Opponent has moved yet
        if opponents_move == -1:
            next_move = random.randrange(0,9,2)
        # Respond to opponents first move
        else:
            self.__current_state[opponents_move] = self.__opponent
            
            if opponents_move == 4:
                next_move = random.choice([0, 2, 6, 8])
            elif opponents_move == 0 or opponents_move == 2 or \
                 opponents_move == 6 or opponents_move == 8:
                next_move = 4
            else:
                next_move = random.choice([0, 2, 4, 6, 8])
                
        self.__current_state[next_move] = self.__player
        
        return next_move
        
    def __findSecondMove(self, opponents_move):
        next_move = -1
        computers_first_move, opponents_first_move = self.__getFirstMoves()
        self.__current_state[opponents_move] = self.__opponent
        
        # Computer moved first
        if opponent_first_move == -1:
            next_move = self.__findMoveWhenComputerMovedFirst(computers_first_move, opponents_move)
        # Opponent moved first
        else:
            next_move = self.__findMoveWhenOpponentMovedFirst(computers_first_move, opponents_first_move, 
                                                               opponents_move)
                                                               
       self.__current_state[next_move] = self.__player

       return next_move
                                                               
   def __findMoveWhenComputerMovedFirst(self, computers_first_move, opponents_move):
       # Computer goes first with center move
       if computers_first_move == 4:
           return self.__findMoveWhenComputerFirstMovedCenter(computers_first_move, opponents_move)
       # Computer goes first with corner move
       else:
           return self.__findMoveWhenComputerFirstMovedCorner(computers_first_move, opponents_move)

    def __findMoveWhenOpponentMovedFirst(self, computers_first_move, opponents_first_move, opponents_move):
        # Opponent goes first with center move
        if opponents_first_move == 4:
            return self.__findMoveWhenOpponentFirstMovedCenter(computers_first_move, opponents_first_move, opponents_move)
        # Opponent goes first with corner move
        elif opponents_first_move == 0 or opponents_first_move == 2 or \
             opponents_first_move == 6 or opponents_first_move ==8:
             return self.__findMoveWhenOpponentFirstMovedCorner(computers_first_move, opponents_first_move, opponents_move)
        # Opponent goes first with edge move
        else:
            return self.__findMoveWhenOpponentFirstMovedEdge(computers_first_move, opponents_first_move, opponents_move)

    def __findMoveWhenComputerFirstMovedCenter(self, computers_first_move, opponents_move):
        # Opponent chose a corner
        if opponents_move == 0:
            return 8
        elif opponents_move == 2:
           return 6
        elif opponents_move == 6:
           return 2
        elif opponents_move == 8:
           return 0
        # Opponent chose an edge
        elif opponents_move == 1:
           return random.choice([6, 8])
        elif opponents_move == 3:
           return random.choice([2, 8])
        elif opponents_move == 5:
           return random.choice([0, 6])
        elif opponents_move == 7:
           return random.choice([0, 2])
        
    def __findMoveWhenComputerFirstMovedCorner(self, computers_first_move, opponents_move):
        # Opponent chose the center
        if opponents_move == 4:
            if computers_first_move == 0:
                return 8
            elif computers_first_move == 1:
                return 7
            elif computers_first_move == 2:
                return 6
            elif computers_first_move == 3:
                return 5
            elif computers_first_move == 5:
                return 3
            elif computers_first_move == 6:
                return 2
            elif computers_first_move == 7:
                return 1
            elif computers_first_move == 8:
                return 0
        # Opponent chose another square
        else:
            if computers_first_move == 0:
                if opponents_move == 2 or opponents_move == 3 or opponents_move == 5:
                    return 6
                else:
                    return 2
            elif computers_first_move == 2:
                if opponents_move == 0 or opponents_move == 1 or opponents_move == 3:
                    return 8
                else:
                    return 0
            elif computers_first_move == 6:
                if opponents_move == 0 or opponents_move == 1 or opponents_move == 3:
                    return 8
                else:
                    return 0
            elif computers_first_move == 8:
                if opponents_move == 3 or opponents_move == 6 or opponents_move == 7:
                    return 2
                else:
                    return 6
                
    def __findMoveWhenOpponentFirstMovedCenter(self, computers_first_move, opponents_first_move, opponents_move):
        # Opponent moves into the opposite corner
        if computers_first_move == 0 and opponents_move == 8:
            return 2
        elif computers_first_move == 2 and opponents_move == 6:
            return 0
        elif computers_first_move == 6 and opponents_move == 2:
            return 8
        elif computers_first_move == 8 and opponents_move == 0:
            return 6
        # Opponent goes for win so block them
        else:
            return 8 - opponents_move
        
    def __findMoveWhenOpponentFirstMovedCorner(self, computers_first_move, opponents_first_move, opponents_move):
        # Opponent forms a diagonal with you
        if (opponents_first_move == 0 and opponents_move == 8) or \
           (opponents_first_move == 8 and opponents_move == 0) or \
           (opponents_first_move == 2 and opponents_move == 6) or \
           (opponents_first_move == 6 and opponents_move == 2):
            return random.choice([1, 3, 5, 7])
        elif opponents_first_move == 0:
            position = self.__findPositionToBlock(opponents_first_move, opponents_move)
            
            if position != -1:
                return position
            elif opponents_move == 5:
                return 2
            elif opponents_move == 7:
                return 6
        elif opponents_first_move == 2:
            position = self.__findPositionToBlock(opponents_first_move, opponents_move)
            
            if position != -1:
                return position
            elif opponents_move == 3:
                return 1
            elif opponents_move == 7:
                return 8
        elif opponents_first_move == 6:
            position = self.__findPositionToBlock(opponents_first_move, opponents_move)
            
            if position != -1:
                return position
            elif opponents_move == 1:
                return 0
            elif opponents_move == 5:
                return 8
        elif opponents_first_move == 8:
            position = self.__findPositionToBlock(opponents_first_move, opponents_move)
            
            if position != -1:
                return position
            elif opponents_move == 1:
                return 2
            elif opponents_move == 3:
                return 6
        
    def __findMoveWhenOpponentFirstMovedEdge(self, computers_first_move, opponents_first_move, opponents_move):
        position = self.__findPositionToBlock(opponents_first_move, opponents_move)
        
        if position != -1:
            return position
        else:
            open_positions = set( self.__findOpenPositions(self.__current_state) )
            good_positions = open_positions - set(1, 3, 5, 7)
            return random.choice(list(good_positions))
        
    def __findOptimalMove(self, opponents_move):
        self.__current_state[opponents_move] = self.__opponent
        open_positions = self.__findOpenPositions(self.__current_state)
        
        if len(open_positions) == 0:
            return -1
        
        self.__solutions = self.__generateNodes(self.__current_state, self.__player)
        
        next_move = -1
        winning_moves = self.__winningMoves(self.__player, self.__current_state)
        if len(winningMoves) != 0:
            next_move = winning_moves[0]
            
        losing_moves = self.__winningMoves(self.__opponent, self.__current_state)
        if len(losing_moves) != 0:
            next_move = losing_moves[0]
            
        if next_move != -1:
            next_move = self.__findHighestScoreNode().move
            
        self.__current_state[next_move] = self.__player
        
        return next_move
                   
    def __generateNodes(self, current_state, player):
        open_positions = self.__findOpenPositions(current_state)

        if len(open_positions) == 1:
            new_state = copy.deepcopy(current_state)
            next_position = open_positions.pop()
            new_state[next_position] = player
            return [ Node(next_position, new_state, self.__calculateGameScore(new_state)) ]

        nodes = []
        for next_position in open_positions:
            new_state = copy.deepcopy(current_state)
            new_state[next_position] = player
            score = self.__calculateGameScore(new_state)
            links = []
            if score == 0:
                next_player = self.__getOtherPlayer(player)
                links = self.__generateNodes(new_state, next_player)
                score = self.__findScore(player, links)
                
            node = Node(next_position, new_state, score, links)
            nodes.append(node)

        return nodes  
        
    def __findOpenPositions(self, current_state):
        open_positions = []
        for i, state in enumerate(current_state):
            if state == TicTacToe.empty_position:
                open_positions.append(i)
        return open_positions
        
    def __getFirstMoves(self):
        moves = [None, None]
        for i, state in enumerate(self.__current_state):
            if state == self.__player:
                moves[0] = i
            elif state == self.__opponent:
                moves[1] = i
                
        return moves
        
    def __findPositionToBlock(self, first_move, second_move):
        for combo in ComputerPlayer.__winning_combinations:
            c = list(combo)
            if first_move in c and second_move in c:
                c.remove(first_move)
                c.remove(second_move)
                return c[0]
                
        return -1
            
    def __calculateGameScore(self, game_state):
        # Find if there is a winner
        if (self.__player == TicTacToe.players[0]) and (self.__isWinner(TicTacToe.players[0], game_state) == True):
            return ComputerPlayer.__winning_score
        elif (self.__player == TicTacToe.players[1]) and (self.__isWinner(TicTacToe.players[1], game_state) == True):
            return ComputerPlayer.__winning_score
        elif (self.__player == TicTacToe.players[1]) and (self.__isWinner(TicTacToe.players[0], game_state) == True):
            return -ComputerPlayer.__winning_score
        elif (self.__player == TicTacToe.players[0]) and (self.__isWinner(TicTacToe.players[1], game_state) == True):
            return -ComputerPlayer.__winning_score
        # Find a good move
        #if (self.__player == TicTacToe.players[0]) and (self.__almostWinner(TicTacToe.players[0], game_state) == True):
        #    return ComputerPlayer.__good_score
        #elif (self.__player == TicTacToe.players[1]) and (self.__almostWinner(TicTacToe.players[1], game_state) == True):
        #    return ComputerPlayer.__good_score
        #elif (self.__player == TicTacToe.players[1]) and (self.__almostWinner(TicTacToe.players[0], game_state) == True):
        #    return -ComputerPlayer.__good_score
        #elif (self.__player == TicTacToe.players[0]) and (self.__almostWinner(TicTacToe.players[1], game_state) == True):
        #    return -ComputerPlayer.__good_score
                
        return 0
        
    def __isWinner(self, player, game_state):
        for combination in self.__winning_combinations:
            if combination[0] == player and combination[1] == player and combination[2] == player:
                return True
                
        return False
        
    def __winningMoves(self, player, game_state):
        winningMoves = []
        for combo in self.__winning_combinations:
            moves = list(combo)
            for position in combo:
                if game_state[position] == player:
                    moves.remove(position) 
                    
            if len(moves) == 1:
                winningMoves.append(moves[0])
                
        return winningMoves
        
    def __almostWinner(self, player, game_state):
        pass
                          
    def __getOtherPlayer(self, player):
        if player == TicTacToe.players[0]:
            return TicTacToe.players[1]
        
        return TicTacToe.players[0]
        
    def __findScore(self, player, links):
        score = 0
        # Max
        if player == self.__player:
            score = -ComputerPlayer.__winning_score
            for node in links:
                if node.score > score:
                    score = node.score
        # Min
        else:
            score = ComputerPlayer.__winning_score
            for node in links:
                if node.score < score:
                    score = node.score
                        
        return score
        
    def __findHighestScoreNode(self):
        score = -1  
        index_of_node = 0
        for i, node in enumerate(self.__solutions):
            if node.score > score:
                score = node.score
                index_of_node = i
                
        return self.__solutions[index_of_node]
                
if __name__ == '__main__':
    # Simple test of the class
	player = ComputerPlayer(TicTacToe.players[0])
	opponent_marker = TicTacToe.players[1]
	
	def printGame(game_state):
	    print " " + str(game_state[0]) + " | " + str(game_state[1]) + " | " + str(game_state[2]) + "\n" + \
              " " + str(game_state[3]) + " | " + str(game_state[4]) + " | " + str(game_state[5]) + "\n" + \
              " " + str(game_state[6]) + " | " + str(game_state[7]) + " | " + str(game_state[8]) + "\n" 
	
	move = 1
	game_over = False
	while 1:
	    open_positions = player._ComputerPlayer__findOpenPositions(player._ComputerPlayer__current_state)
	    opponents_move = random.choice(open_positions)
	    players_move = player.getNextMove( opponents_move )
	     
	    if players_move == -1:
	        game_over = True
	     
	    print "Turn:  " + str(move)
	    print "Opponent moves: " + str(opponents_move)
	    print "Players moves: " + str(players_move)
	    move += 1
	    
	    if player._ComputerPlayer__isWinner(player._ComputerPlayer__player, player._ComputerPlayer__current_state):
	        print "Computer wins!!!"
	        game_over = True
	    elif player._ComputerPlayer__isWinner(opponent_marker, player._ComputerPlayer__current_state):
	        print "Opponent wins :("
	        game_over = True
	    
	    print
	    printGame(player._ComputerPlayer__current_state)
	    print
	    
	    if game_over:
	        break
	    

