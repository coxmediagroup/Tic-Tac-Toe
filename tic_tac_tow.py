"""
 TIC-TAC-TOW; Terminator Vs Human: Tic Tac Toe. version: .07
 Copyright (C) 2011 John Lutz

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 as published by the Free Software Foundation; either version 2
 of the License, or (at your option) any later version.
 
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
 
 I can be reached at JohnnyLutz@gmail.com
"""
import random


class Paper():
    """Paper to mark off X or O between Computer and Player"""
    board = [ ['A', 'B', 'C'],
              ['D', 'E', 'F'],
              ['G', 'H ','I']
    # class note definitions of mark are coordinates of row,col
    def __init__(self):
        # invisible board with all applicable possible moves that are left.
        # it's one of the few things that are not normalized because of neatness
        # and effeciency
        self.board_moves_remaining = board

    #location on board as 'mark' in coordinates    
    def set_mark(self, (row,col), mark):
        self.board[row,col] = mark

    def get_mark(self, (row, col)):
        return self.board[row,col]

    def convert_alpha_to_mark(self, alpha):
        """ Convert a letter to a coordinate mark """
        entire_board = ord(alpha) - ord('a')  
        row = entire_board / 3
        col = entire_board % 3
        return (row, col)

    def convert_mark_to_alpha(self, mark):
        """ Convert a coordinate mark to a letter  """
        (row, col) = mark
        return chr(ord('a') + row*3 + col)

    def is_location_blank(self, board_location):
        test_square= paper.get_mark(board_location)
        if (test_square != 'X' && test_square !='O')
            return true;

    def is_new_board(self):
        for mark in board:
            if (!self.if_location_blank(convert_alpha_to_mark(mark)):
                return false
        return true
    # JKL TODO: + testing + debugging
    def get_diagnals_opposite_empty(self, mark):
         
    def get_middle_opposite_empty(self, mark):

    def is_corner_of(self):
        
    def is_middle_of(self):

    def is_next_to(self):

    def print_current_board(self):
        """ print rows of board of current state """
        for i in range(2):
            print get_mark(i,i) , " | " , get_mark(i,i+1), " | ", get_mark(i,i+2)
            if (i < 2):
                print ---+---+---

class Player():
    """generic player"""
    
    current_moves = [[]]
  
    def __init__(mark_type):
        set_mark_type(mark_type)
        self.won = false
        self.tie = false:

    def make_move(alpha,paper):
        # check to see if a move already took place on this location
        at_location = paper.convert_alpha_to_mark(alpha)

        # is coord on screen not used? if so set it on the paper and record the
        # move for the player.
        if( (paper.is_location_blank() ):
            paper.set_mark(at_locaton, get_mark_type()) 
            current_moves.append( at_location )
            current_moves.sort()

            paper.board_moves_remaining.remove( at_location )
            return true
        return false   # Not a valid move, mark location already set   
            
    def set_mark_type(self, symbol_type)
        self.mark = symbol_type

    def get_mark_type(self)
        return self.mark 

    def opposite_mark_type(self):
        if ('X' in self.get_mark_type())  #switcharoo for outter objects 
            return 'O'
        else:
            return 'X'
    
   
class Person(Player):
    def __init__(self):

    def inputs(self, paper):
        while True:
            of_response_box = raw_input("Enter a valid board-letter:")
            if(make_move(of_response_box, paper)):
                return       # return to main loop 
             
    
class Computer(Player):
    """Ruthless Terminator destined to make computer and human tie """
    priority_rows=[]   # priority (most filled) + actual row (in sort order)

    def __init__(self, mark_type):
        if (trim(mark_type) == ''):   #no mark_type?
           mark_type_value = random.randint(0,1)

           if (mark_type_value == 0):  # have terminator select
               set_mark_type('X')
           else
               set_mark_type('O') 

    def response(self, paper):
        # Scan center, if not set, center gets the square
        # only real rule for AI, rest is all just priotity hashing
        if (paper.is_location_blank(convert_alpha_to_mark('E') ) ):
            if (make_move(paper.convert_alpha_to_mark('E') ) ):  
                return  # usually happens at the begining, hence here


        # AI search and set 
        for row_remaining in convert_alpha_to_mark(paper.moves_remaining()):
            for row,col in row_remaining:
                # is functions will return a valid row or false
                # orfer of test is important
                # Since this is AI, it remains here
                #  never a center piece
                if(paper.is_corner_of(row,col)):
                    cross_check = paper.get_diagnal_opposite_empty((row,col))
    
                elif(paper.is_middle_of(row,col)):         
                    cross_check = paper.get_middle_opposite_empty((row,col))
                
                else(paper.is_next_to((row,col))):
                    make_move(cross_check, paper)
                    return

                # diagnal or middle set
                if (cross_check):
                    make_move(cross_check, paper)
                    return
   
class Game():
    # each game has a paper, player, computer and all winning combinations
     """All possible winning combinations"""
    winning_rows = [ [0,3,6],[1,4,7],[2,5,8],      # vertical 
                     [0,1,2],[3,4,5],[6,7,8],      # horizontal
                     [0,4,8],[2,4,6]]              # diagonal
    

    def __init__(self):
        print "Would you prefer a nice game of tic-tac-toe? :)"
        goes_first = raw_input("Who goes first; Computer or Human?")

        if (goes_first == "C" ):     #Does computer go first?
            self.computer = Computer('')     # randomly generate mark type
            self.person = Person(self.computer.opposite_mark_type())
        else:   
            mark_type = raw_input("Would you like X or O?")
            self.person = Person(mark_type)
            self.computer = Computer(self.player.opposite_mark_type())

        self.on_scratch_paper = Paper()
               
    def game_loop(self):
        while True :
            ### if we aren't finished, perform human's turn
            if(is_finished(on_scratch_paper)):
                break;
            person.inputs(on_scratch_paper)

            ### If we aren't finished, switch to computer's turn
            if(is_finished(on_scratch_paper)):
                break;
            computer.response(on_scratch_paper)
            
            on_scratch_paper.print_current_board()
    
        print "final board="
        self.on_scratch_paper.print_current_board()

    # brute force, refactor into a weighting system for expansion into > 3x3
    def is_finished(self):
        self.computer.won = self.player.won = self.computer.tie = false
        for win_test in winning_rows:
            win_or_tie(win_test, self.player)
            win_or_tie(win_test, self.computer)

        if (self.computer.won || \
            self.player.won   || \
            self.computer.tie):
            return true
        else
            return false

    # helper procedure
    def win_or_tie(self, win_test, playa):
        if(win_test in playa.current_moves):
            if (playa.current_moves.length() == 2):  # 3 moves
                player.won = true
            if (playa.current_moves.length() > 2):   # > 3 moves
                computer.tie = true

    def game_results(self):
        if(self.player.won):         
            print "You won! Terminator is dust."     #should never happen
        elif (self.computer.tie):  
            print "Strange game, the only winning move is not to play."     #will likely always happen
        else(self.computer.won)
            print "The computer won; thats what it does, thats all it does!"
        
        return true

if __name__ == "__main__":

    tic_tac_toe = Game()    
    tic_tac_toe.game_loop()
    tic_tac_toe.game_results()

