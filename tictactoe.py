#!/usr/bin/env python

import operator
import sys
import random


def allEqual(list):
    """returns True if all the elements in a list are equal, or if the list is empty."""
    return not list or list == [list[0]] * len(list)

Empty = ' '
Player_X = 'x'
Player_O = 'o'

class Board:
    """This class represents a tic tac toe board state."""
    def __init__(self):
        """Initialize all members."""
        self.pieces = [Empty]*9
        self.field_names = '123456789'

    def output(self):
        """Display the board on screen."""
        for line in [self.pieces[0:3], self.pieces[3:6], self.pieces[6:9]]:
            print ' | '.join(line)

    def winner(self):
        """Determine if one player has won the game. Returns Player_X, Player_O or None"""
        winning_rows = [[0,1,2],[3,4,5],[6,7,8], # vertical
                        [0,3,6],[1,4,7],[2,5,8], # horizontal
                        [0,4,8],[2,4,6]]         # diagonal
        for row in winning_rows:
            if self.pieces[row[0]] != Empty and allEqual([self.pieces[i] for i in row]):
                return self.pieces[row[0]]

    def getValidMoves(self):
        """Returns a list of valid moves. A move can be passed to getMoveName to 
        retrieve a human-readable name or to makeMove/undoMove to play it."""
        return [pos for pos in range(9) if self.pieces[pos] == Empty]

    def gameOver(self):
        """Returns true if one player has won or if there are no valid moves left."""
        return self.winner() or not self.getValidMoves()

    def getMoveName(self, move):
        """Returns a human-readable name for a move"""
        return self.field_names[move]
    
    def makeMove(self, move, player):
        """Plays a move. Note: this doesn't check if the move is legal!"""
        self.pieces[move] = player
    
    def undoMove(self, move):
        """Undoes a move/removes a piece of the board."""
        self.makeMove(move, Empty)

def humanPlayer(board, player):
    """Function for the human player"""
    board.output()
    possible_moves = dict([(board.getMoveName(move), move) for move in board.getValidMoves()])
    move = raw_input("Enter your move (%s): " % (', '.join(sorted(possible_moves))))
    while move not in possible_moves:
        print "Sorry, '%s' is not a valid move. Please try again." % move
        move = raw_input("Enter your move (%s): " % (', '.join(sorted(possible_moves))))
    board.makeMove(possible_moves[move], player)

def computerPlayer(board, player):
    """Function for the computer player"""

    board.output()
    opponent = { Player_O : Player_X, Player_X : Player_O }

    def judge(winner):
        if winner == player:
            return +1
        if winner == None:
            return 0
        return -1

    def evaluateMove(move, p=player):
        try:
            board.makeMove(move, p)
            if board.gameOver():
                return judge(board.winner())
            outcomes = (evaluateMove(next_move, opponent[p]) for next_move in board.getValidMoves())

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
            board.undoMove(move)

    moves = [(move, evaluateMove(move)) for move in board.getValidMoves()]
    random.shuffle(moves)
    moves.sort(key = lambda (move, winner): winner)
    
    print moves
    board.makeMove(moves[-1][0], player)

def game():
    """The game function"""
    b = Board()
    turn = 1
    while True:
        print "%i. turn" % turn

        humanPlayer(b, Player_O)
        if b.gameOver(): 
            break
        computerPlayer(b, Player_X)

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

