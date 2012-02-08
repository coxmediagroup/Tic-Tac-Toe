# -*- coding: utf-8 -

#  Tic-Tac-Toe excercise
#
#  Authors: Lucia Gonzalez, Alan Descoins
#  e-mail: lucia@tryolabs.com, alan@tryolabs.com
#
#                               Tryolabs - Feb 2012
#

import operator
import sys
import random
import string

def allEqual(list):
    """returns True if all the elements in a list are equal, or if the list is empty."""
    return not list or list == [list[0]] * len(list)

Empty = ' '
Player_X = 'X'
Player_O = 'O'
Size = 1
# Maximum search depth for board size > 3
max_prof = 3
# Minimum number of free spots after which max_prof has no effect
min_free_spots = 9

class Board:
    """This class represents a tic tac toe board state."""
    def __init__(self):
        """Initialize all members."""
        self.spots = [Empty] * (Size * Size)
        self.free_spots = Size * Size

    def printBoard(self):
        """Display the board status on screen."""
        for i in range(Size):
            if self.spots[i * Size] == Empty:
                print chr(27) + "[0;92m" + '%2d' % (i * Size) + chr(27) + "[0;m",
            elif self.spots[i * Size] == Player_X:
                print chr(27) + "[0;91m " + self.spots[i * Size] + chr(27) + "[0;m",
            else:
                print chr(27) + "[0;94m " + self.spots[i * Size] + chr(27) + "[0;m",
            for j in range(1,Size):
                print chr(27) + "[0;90m" + "|" + chr(27) + "[0;m",
                if self.spots[i * Size + j] == Empty:
                    print chr(27) + "[0;92m" + '%2d' % (i * Size + j) + chr(27) + "[0;m",
                elif self.spots[i * Size + j] == Player_X:
                       print chr(27) + "[0;91m" + '%2s' % (self.spots[i * Size + j]) + chr(27) + "[0;m",
                else:
                    print chr(27) + "[0;94m" + '%2s' % (self.spots[i * Size + j]) + chr(27) + "[0;m",
            print
            if i != Size - 1:
                print chr(27) + "[0;90m" + "-" * Size * 5 + chr(27) + "[0;m"

    def checkDiagonal(self, direction):
        """Searches for a winner in the diagonals of the board"""
        if direction == 1:
            piece = self.spots[0]
        elif direction == -1:
            piece = self.spots[Size - 1]
        if piece != Empty:
            for i in range(1, Size+1):
                if (i * (Size + direction) < (Size * Size)) and piece != self.spots[i * (Size + direction)]:
                    return False    
            return True
        return False

    def checkHorizontal(self, position):
        """Searches for a winner in a row of the board"""
        if self.spots[position] != Empty:
            return allEqual([self.spots[position] for position in range(position, position + Size)])
        return False

    def checkVertical(self, position):
        """Searches for a winner in a column of the board"""
        if self.spots[position] != Empty:
            for i in range(1, Size):
                if self.spots[position] != self.spots[i * Size + position]:
                    return False
            return True
        return False

    def winner(self):
        """Determine if one player has won the game. Returns which one won or None"""
        # Checks diagonal
        if self.checkDiagonal(1):
            return self.spots[0]
        if self.checkDiagonal(-1):
            return self.spots[Size - 1]
        
        # Checks Horizontal
        for i in range(Size):
            if self.checkHorizontal(i * Size):
                return self.spots[i * Size]
        
        # Checks Vertical
        for i in range(Size):
            if self.checkVertical(i):
                return self.spots[i]        

    def getValidMoves(self):
        """Returns a list of valid moves."""
        return [pos for pos in range(Size * Size) if self.spots[pos] == Empty]

    def gameOver(self):
        """Returns true if one player has won or if there are no valid moves left."""
        return self.winner() or not self.getValidMoves()
    
    def makeMove(self, move, player):
        """Plays a move."""
        self.spots[move] = player
        if player != Empty:
            self.free_spots -= 1
        else:
            self.free_spots += 1
    
    def undoMove(self, move):
        """Removes a piece of the board."""
        self.makeMove(move, Empty)

def humanPlayer(board, player):
    """Function for the human player."""
    possible_moves = board.getValidMoves()
    move = int(raw_input("Enter your move (%s): " % (', '.join(map(str,possible_moves)))))
    while move not in possible_moves:
        print "Sorry, '%s' is not a valid move. Please try again." % move
        move = int(raw_input("Enter your move (%s): " % (', '.join(map(str,possible_moves)))))
    board.makeMove(move, player)

def computerPlayer(board, player):
    """Function for the computer player."""
    opponent = { Player_O : Player_X, Player_X : Player_O }

    def judge(winner):
        if winner == player:
            return +1
        if winner == None:
            return 0
        return -1

    def evaluateMove(move, p = player, prof = 0, limit_recursion = True):
        """Evaluates the next move using the Minimax decision rule."""
        try:
            board.makeMove(move, p)
            if max_prof != -1 and limit_recursion:
                if prof >= max_prof:
                    return 0
            if board.gameOver():
                return judge(board.winner())
            outcomes = (evaluateMove(next_move, opponent[p], prof + 1, limit_recursion) for next_move in board.getValidMoves())
            if p == player:
                min_element = 1
                for o in outcomes:
                    if o == -1:
                        return o
                    min_element = min(o,min_element)
                return min_element
            else:
                max_element = -1
                for o in outcomes:
                    if o == +1:
                        return o
                    max_element = max(o,max_element)
                return max_element
        finally:
            board.undoMove(move)

    moves = [(move, evaluateMove(move, player, 0, board.free_spots > min_free_spots)) for move in board.getValidMoves()]
    random.shuffle(moves)
    moves.sort(key = lambda (move, winner): winner)
    board.makeMove(moves[-1][0], player)

def game():
    """The game function"""
    # First asks for the size of the board
    global Size
    Size = raw_input("Please enter the size of the board: ")
    while Size == "" or int(Size) < 3:
        print "Sorry, '%s' is not a valid size for the board." % Size
        Size = raw_input("Please enter the size of the board: ")
    Size = int(Size)

    # If the size of the board is 3x3, does not limit the depth of the search by setting max_prof in -1
    if Size == 3:
        global max_prof
        max_prof = -1

    # Asks if the human wants to start
    first = raw_input("Would you like to start? (yes/no): ")
    while first == "" or (string.find('yes', first) == -1 and string.find('no', first) == -1):
        print "Incorrect answer"
        first = raw_input("Would you like to start? (yes/no): ")

    # Creates the board
    b = Board()

    if string.find('yes', first) == -1:
        print "My turn."
        computerPlayer(b, Player_X)

    while True:
        b.printBoard()
        print "Your turn.",
        humanPlayer(b, Player_O)
        if b.gameOver(): 
            break
        b.printBoard()
        print "My turn."
        computerPlayer(b, Player_X)
        if b.gameOver(): 
            break

    b.printBoard()
    if b.winner():
        print 'Player "%s" wins' % b.winner()
    else:
        print 'Game over'

if __name__ == "__main__":
    game()

