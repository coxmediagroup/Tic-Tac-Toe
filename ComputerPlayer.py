import copy
import random
from random import randint
from utils import debug_print as d_pr
from itertools import permutations

class ComputerPlayer(object):
    
    
    #x_or_o should be 'x' or 'o'
    def __init__(self, x_or_o, the_board):
        
        # 'x' if the player is x and 'o' elsewise
        self.x_or_o = x_or_o 
        self.the_board = the_board
        
        #not sure if necessary, just in case
        random.seed()
        
    
    #not actually used by this program, but since it helps test GetOutcomeOfMoveSequence, i'm leaving it
    def is_move_win_for_me(self, row_and_col):
        
        outcome = self.GetOutcomeOfMoveSequence({'player' : self.x_or_o, 'move' : row_and_col})
        
        return outcome==self.x_or_o
    
    
    

    #pick an empty square on the board at random
    def GetRandomMove(self, empty_sq):
        rand_indx= randint(0, len(empty_sq)-1)
        return empty_sq[rand_indx]
    

    
    #this returns a list of moves that the computer could make that would
    # give the computer 2-in-a-row i.e. a 'threat' to the human player 
    # because the computer would win on the following move
    # however, any such moves are not counted if they lead the computer into a 'trap'
    # a situation where the human player would have two ways to win after the human
    # blocked the computer's attempt to get 3-in-a row
    
    def GetThreateningMovesWithoutTraps(self, empty_sq):
        
        
        #all moves the computer could make to win right now
        winning_moves = self.the_board.GetWinningMovesFor( 'computer')
        
        d_pr('winning moves: ' + str(winning_moves))
        
        
        #all moves the computer could make now *except* the ones where he would win
        
        moves_minus_wins = [x for x in empty_sq if x not in winning_moves]
        
        
        #all possible pairs of moves the computer could take to win if theoretically the computer
        #could go twice in a row, skippng the human's turn
        # this is used to calculate ways to attempt to get 3-in-a-row in order to win
        
        all_possible_non_winning_move_pairs = list(permutations(moves_minus_wins,r=2))
        
        d_pr('all possible non win pairs' + str(all_possible_non_winning_move_pairs))
        
        threatening_move_list=[]
        
        for m in all_possible_non_winning_move_pairs:
            move_seq = [{'player': self.x_or_o, 'move': m[0]}, {'player': self.x_or_o, 'move': m[1]}]
            
       
            #if two moves together make a win, then they qualify as 'threats' as each move
            #would set up a 2-in-a-row
            
            if self.the_board.GetOutcomeOfMoveSequence(move_seq)==self.x_or_o:
                
                #make sure each does not lead to a trap
                
                #pretend computer makes the first move and  human makes the other move to block the 3-in-arow
                temp_board=self.the_board.GetBoardWithSimulatedMove([move_seq[0], {'player': self.the_board.human_player_x_or_o, 'move': m[1]}])
                
                
                #this is the number of ways the human could now win after the given two moves are made
                # if it's more than one that means these moves can lead to a trap
                # and we should not use this move as an option for the computer
                
                wins_for_human_if_move_1 = temp_board.GetWinningMovesFor( 'human')
                
                d_pr('if comp moves ' + str(m[0]))
                d_pr('then human moves ' + str(m[1]))
                d_pr('human wins by: ' + str(wins_for_human_if_move_1))
                
                # if the human can win in 1 or zero ways after this move
                #then this move is an ok 'threat' to make
                # 2 or more and this a trap and must be avoided
                
                
                if len(wins_for_human_if_move_1) < 2:
                    if m[0] not in threatening_move_list:
                        threatening_move_list.append(m[0])
                
                else:
                    d_pr('move ' + str(m[0]) + ' leads to a trap')
                
                
                #now try it if computer makes the second move and humans makes the first to block the 3-in-a-row
                
                temp_board=self.the_board.GetBoardWithSimulatedMove([move_seq[1], {'player': self.the_board.human_player_x_or_o, 'move': m[0]}  ])
                
                wins_for_human_if_move_2 = temp_board.GetWinningMovesFor('human')
                
                d_pr('if comp moves ' + str(m[1]))
                d_pr('then human moves ' + str(m[0]))
                
                d_pr('human wins by: ' + str(wins_for_human_if_move_2))
                
                
                
                if len(wins_for_human_if_move_2) < 2:
                    if m[1] not in threatening_move_list:
                        threatening_move_list.append(m[1])
                
                else:
                    d_pr('move ' + str(m[1]) + ' leads to a trap')

        return threatening_move_list


    
    def GetNextMove(self, empty_sq):
        
        #Here's the most important algorithm:
        #If this is the first move: take the middle if possible, else take the first corner
        # Win if possible
        # else: Block any wins by the human else
        # else: threaten the player by assembling 2 in a row in the first available square that you can
        # UNLESS choosing that square brings about a board configuration where the human can win
        # in more than one possible way i.e. a trap
        # else if there is no way to threaten the player with 2-in-a-row and without a trap, then 
        # choose a random square
        
        #if it's the first or second move of the game, i.e. 8 or 9 empty squares left
        if len(empty_sq) > 7:
            
            #if middle square is empty, choose that move
            if [1,1] in empty_sq:
                return [1,1]
            
            if [0,0] in empty_sq:
                return [0,0]
            
            # we should never reach here
            
            raise Exception("should never have more than 7 empty squares without middle or top-left being empty")
        
        #ok so it's not the first or second move:
        
        
        #1. win if you can
        
        winning_moves = self.the_board.GetWinningMovesFor('computer')
        
        #return first winning move
        if winning_moves != []:
          return winning_moves[0]
        
        #2. Block any wins by the human
        
        possible_winning_move_for_opponent = self.the_board.GetWinningMovesFor(which_player='human')
        
        if possible_winning_move_for_opponent != []:
            #if more than one, we'll lose but just take the first move
            #should never actually happen
            return possible_winning_move_for_opponent[0]
        
        #3.OK so the other side can't win right now
        #now try to make 2-in-a-row to 'threaten' the opponent
        # but don't lead yourself into a trap
        
        threaten_without_trap_moves = self.GetThreateningMovesWithoutTraps(empty_sq)
        
        #return first one
        if threaten_without_trap_moves != []:
            return threaten_without_trap_moves[0]
        
        
        #BIG ASSUMPTION WHICH IS PROB TRUE: it will never happen that i can threaten but only threaten into a trap
        # so if there are no threatening moves that don't lead to traps, there are no threatening moves at all
        # so i can just make a random move
        d_pr('no threats available to use: making random move')
        
        return self.GetRandomMove(empty_sq)
        
        
    
    
    
    
    def MakeMove(self):
        
        empty_sq = self.the_board.GetEmptySquares()
        
        d_pr('Number of empty squares is ' + str(len(empty_sq)) )
        
        d_pr ('empty squares are ' + str(empty_sq))
        
        #next_move=self.MakeRandomMove(empty_sq)
        
        next_move = self.GetNextMove(empty_sq)
        
        self.the_board.MakeMove(next_move)
        
        d_pr('Computer chose space at ' + str(next_move))
        
        
        #if computer one, tell the Board
        if self.the_board.IsWinningBoard() != None:
            self.the_board.SetGameOver(self.the_board.IsWinningBoard())
        


class RandomPlayer(object):
    
    def __init__(self, the_board):
        self.the_board = the_board
    
    def GetNextMove(self):
        return self.GetRandomMove(self.the_board.GetEmptySquares())
        
        
    def GetRandomMove(self, empty_sq):
        rand_indx= randint(0, len(empty_sq)-1)
        return empty_sq[rand_indx]
    
