#
#Cox Media Group 'Tic-Tac-Toe' Coding Challenge
#Author: Samuel Aparo
#Created on Mar 5, 2011
#

#Board Class: A class to represent a simple 3x3 tic-tac-toe board. Essentially, it provides an 
#interface to the board data structure to ensure that only valid moves are read and written. 
#It is also able to 'print' itself. 
class Board:
    
    #Constructor. Initialize board data structure (a list of lists)
    def __init__(self):
        #Game Board Value Key: 0=Empty, 1=X, 2=O
        self.gameBoard = [[0,0,0],[0,0,0],[0,0,0]]
        
    #Update Board Method. Takes in a row, column, and an 'X' or 'O' to put there. 
    #Returns true if update was successful, false otherwise. 
    def updateBoard(self, row, col, mark):
        pass
    
    #Read Board Method. Takes in a row and column. Returns an 'X', 'O', 'N' (for empty), or 'E' for 
    #an invalid space. 
    def readBoard(self, row,col):
        pass
    
    #Render Board Method. Outputs the contents of the board to the screen.
    def renderBoard(self):
        pass

#Make Next Move Function: Algorithm that makes computer player's next move, and modifies the board
#accordingly. 
def MakeNextMove(gameBoard):
    pass

#Is Game Over Function: Algorithm for determining if the game is over.
def isGameOver(gameBoard):
    pass

#Main Function. Procedure for playing a game. Ties together Board, AI, and user input. 
if __name__ == '__main__':
    pass
    