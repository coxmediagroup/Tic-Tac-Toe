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
    
    #Update Board Method. Takes in a row, column, and a mark to put there. 
    #Returns true if update was successful, false otherwise. 
    def updateBoard(self, row, col, mark):
        #If Board Location Is Valid (i.e. readBoard returns something other than -1),
        #attempt to save provided mark
        if(self.readBoard(row, col) != -1):
            self.gameBoard[row][col] = mark
            return True
        #Otherwise, return False
        else:
            return False
    
    #Read Board Method. Takes in a row and column. Returns a 0,1,2, or -1 for 
    #an invalid space. 
    def readBoard(self, row,col):
        #Check to see if provided space is valid. 
        validRow = 0<=row<3
        validCol = 0<=col<3
        if(validRow and validCol):
            #Return mark at current location
            return self.gameBoard[row][col]
        else:
            return -1
    
    #Render Board Method. Returns a string representing board.
    def renderBoard(self):
        output=''
        for r in range(3):
            for c in range(3):
                markAtLocation = self.readBoard(r, c)
                correspondingSymbol=''
                if(markAtLocation==0):
                    correspondingSymbol = '_'
                elif(markAtLocation==1):
                    correspondingSymbol = 'X'
                elif(markAtLocation==2):
                    correspondingSymbol = 'O'
                output += correspondingSymbol+'|'
            output +='\n'
        return output

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
    