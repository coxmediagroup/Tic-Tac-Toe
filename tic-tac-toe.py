#!/usr/bin/env python

import operator
import sys
import random
import pickle


def winningArray(list):
    """returns True if all the elements in a list are equal, or if the list is empty. This is used to determine if a player has 'line' of 3 in a row"""
    return not list or list == [list[0]] * len(list)



EmptyBoardSpace = ' '
Player_x = 'x'
Player_o = 'o'

class TicTacToeBoard:
    """This class represents a tic tac toe board state."""
    def __init__(self):
        """Initialize all members."""

        # attribute for places on board
        # - | - | -
        # - | - | -
        # - | - | -
        ## where '-' is represented by ' ' from EmptyBoardSpace variable
        
        self.board_space = [EmptyBoardSpace]*9
        # the idea here is to make field names understandable by people where as arrays normally start with 0 instead of 1
        # so when needed you chop up string: ie self.field_names[0] would be the equivalent of the first character of the string which is '1'
        self.field_names = '123456789'
        
    
    def output(self):
        """Display the board on screen."""
        ## this is just a list of the board_space array split out by the lines
        ## then joining each of the items in the subarrays with ' | '
        ## the print function when called automatically adds the newline feed to each line so you get your text board
        #  |  | 
        #  |  | 
        #  |  |         
        for line in [self.board_space[0:3], self.board_space[3:6], self.board_space[6:9]]:
            print(' | '.join(line))


    def winner(self):
        """Determine if one player has won the game. Returns Player_x, Player_o or None"""
        winning_rows = [[0,1,2],[3,4,5],[6,7,8], # vertical
                        [0,3,6],[1,4,7],[2,5,8], # horizontal
                        [0,4,8],[2,4,6]]         # diagonal
        for row in winning_rows:
            if self.board_space[row[0]] != EmptyBoardSpace and winningArray([self.board_space[i] for i in row]):
                # return the first item of the winning row
                # a short cut of returning which player has won as the first char of a winning row will be 'x' or 'o'
                return self.board_space[row[0]]

    def getValidMoves(self):
        """Returns a list of valid moves. A move can be passed to getMoveName to 
        retrieve a human-readable name or to makeMove/undoMove to play it.
        board_space that contain a ' ' have not yet been played.
        """
        return [pos for pos in range(9) if self.board_space[pos] == EmptyBoardSpace]

    def gameOver(self):
        """Returns true if one player has won or if there are no valid moves left (empty list)."""
        
        return self.winner() or not self.getValidMoves()

    def getMoveName(self, move):
        """Returns a human-readable name for a move"""
        return self.field_names[move]
    def save(self, filename):
        """save game board object to file to allow for separate calls to the same game
        typically used for web interface
         move count or player tracking would be needed to find who moves next"""
        pickle.dump(self,open(filename, "wb"))
    
    def load(self, filename):
        """load gamesave check if game is complete"""
        lastgame = pickle.load(filename)
        self.board_space = lastgame.board_space
        self.field_names = lastgame.field_names
        if self.gameOver:
            self.output()
            print "game %s already over" % filename
            sys.exit()
    
    def makeMove(self, move, player):
        
        """Plays a move by setting that item of the list to either 'x' or 'o' which is the value of each player.
        Note: this doesn't check if the move is legal!"""
        self.board_space[move] = player
    
    def undoMove(self, move):
        """Undoes a move/removes a piece of the board by setting that list item to ' ' character"""
        self.makeMove(move, EmptyBoardSpace)

def humanPlayer(board, player):
    """Function for the human player"""
    #print board
    board.output()
    #get human readable moves
    possible_moves = dict([(board.getMoveName(move), move) for move in board.getValidMoves()])
    #collect user's move
    move = raw_input("Player %s -Enter your move (%s): " % (player,', '.join(sorted(possible_moves))))
    while move not in possible_moves:
        print "Sorry Player %s, '%s' is not a valid move. Please try again." % (player, move)
        move = raw_input("Enter your move (%s): " % (', '.join(sorted(possible_moves))))
    #find move in human readable dictionary object and make move
    board.makeMove(possible_moves[move], player)

def computerPlayer(board, player):
    """Function for the computer player"""

    board.output()
    # a dictionary object to be used in recursive algorithm to eval opponents game play thru
    # effectively alternating players thru each recursion
    opponent = { Player_o : Player_x, Player_x : Player_o }
    

    def judge(winner):
        if winner == player:
            return +1
        if winner == None:
            return 0
        return -1
    #implement recursive brute force algorithm that calculates all possible outcomes for a move and assigns value
    # -1 for losing move
    # 0 for a move ending in tie
    # +1 for a winning move
            
    def evaluateMove(move, p=player):
        try:
            board.makeMove(move, p)
            if board.gameOver():
                return judge(board.winner())
            outcomes = (evaluateMove(next_move, opponent[p]) for next_move in board.getValidMoves())
            
            print
            if p == player:
                #return min(outcomes)
                min_element = 1
                for o in outcomes:
                    if o == -1:
                        return o
                    min_element = min(o,min_element)
                return min_element
            else:
                #return max(outcomes)
                max_element = -1
                for o in outcomes:
                    if o == +1:
                        return o
                    max_element = max(o,max_element)
                return max_element

        finally:
            #as each recursion exits each simulated move is undone
            #until board reaches original state
            board.undoMove(move)


    # create move list of tuples contain (move, win-lose-tie value)
    moves = [(move, evaluateMove(move)) for move in board.getValidMoves()]

    #since there will be more than one non-losing move randomize pick
    random.shuffle(moves)
    
    moves.sort(key = lambda (move, winner): winner)
    
    # sort and make move with last tuple in list and first item of that tuple
    #[(6, -1), (3, -1), (8, -1), (5, -1), (7, 0), (0, 0), (4, 0), (2, 0)]
    # case above would use 2 for move
    board.makeMove(moves[-1][0], player)

def game():
    """The game function"""
    b = TicTacToeBoard()
    turn = 1
    while True:
        print "%i. turn" % turn

        humanPlayer(b, Player_o)
        if b.gameOver(): 
            break
        computerPlayer(b, Player_x)

        if b.gameOver(): 
            break
        turn += 1
        b.output()

    b.output()
    if b.winner():
        print 'Player "%s" wins' % b.winner()
    else:
        print 'Game over'

if __name__ == "__main__":
    
    game()

