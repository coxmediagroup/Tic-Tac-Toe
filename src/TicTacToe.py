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

#Rotate Board Function. Returns a version of the board 'rotated' 90 degrees clockwise. 
def RotateBoard(gameBoard):
    newBoard = Board()
    for i in range(3):
        for j in range(3):
            newBoard.updateBoard(i, j, gameBoard.readBoard((3-j)-1, i))
    return newBoard


#Is Game Over Function: Algorithm for determining if the game is over. Returns 0 for no, 1 for X win
#2 for 0 win, and -1 for a tie game. 
def isGameOver(gameBoard):    
    #Check for a vertical, horizontal, middle, or diagonal win. If no win was found, rotate board (4 times)
    for i in range(4):
        #Vertical Check
        if((gameBoard.readBoard(0,0)!=0) and (gameBoard.readBoard(0,0)==gameBoard.readBoard(1,0)) and (gameBoard.readBoard(1,0)==gameBoard.readBoard(2,0))):
            return gameBoard.readBoard(0,0)
        #Horizontal Check
        elif ((gameBoard.readBoard(0,0)!=0) and (gameBoard.readBoard(0,0)==gameBoard.readBoard(0,1)) and (gameBoard.readBoard(0,1)==gameBoard.readBoard(0,2))):
            return gameBoard.readBoard(0,0)
        #Middle Check
        elif ((gameBoard.readBoard(1,0)!=0) and (gameBoard.readBoard(1,0)==gameBoard.readBoard(1,1)) and (gameBoard.readBoard(1,1)==gameBoard.readBoard(1,2))):
            return gameBoard.readBoard(1,0)
        #Diagonal Check
        elif ((gameBoard.readBoard(0,0)!=0) and (gameBoard.readBoard(0,0)==gameBoard.readBoard(1,1)) and (gameBoard.readBoard(1,1)==gameBoard.readBoard(2,2))):
            return gameBoard.readBoard(0,0)
        #Rotate Board Otherwise
        else:
            gameBoard = RotateBoard(gameBoard)
            
    #If no win was found, check to see if board is full. If not, return a 'game not over' value
    for i in range(3):
        for j in range(3):
            if(gameBoard.readBoard(i,j)==0):
                return 0
            
    #Otherwise, return 'tie' value
    return -1

#Copy Board Function: Creates a by-value copy of game board
def CopyBoard(gameBoard):
    newBoard = Board()
    for i in range(3):
        for j in range(3):
            newBoard.updateBoard(i, j, gameBoard.readBoard(i, j))
    return newBoard

#Make Next Move Function: Algorithm that decides computer player's next move.
def MakeNextMove(gameBoard):
    #Find a free space that would result in a win or, if winning isn't possible, would block the
    #computer player's win. 
    moveToReturn = [-1,-1]
    lastAvailableFreeSpace = [-1,-1]
    for i in range(3):
        for j in range(3):
            if(gameBoard.readBoard(i,j)==0):
                lastAvailableFreeSpace[0] = i
                lastAvailableFreeSpace[1]= j
                newBoard = CopyBoard(gameBoard)
                newBoard.updateBoard(i,j,1)
                gameStatus = isGameOver(newBoard)
                if(gameStatus==1):
                    moveToReturn[0] = i
                    moveToReturn[1] = j
                    return moveToReturn
                else:
                    newBoard.updateBoard(i,j,2)
                    gameStatus = isGameOver(newBoard)
                    if(gameStatus == 2):
                        moveToReturn[0] = i
                        moveToReturn[1] = j
    #If no BLOCK was found,  attempt to occupy a corner
    if(moveToReturn[0]==-1):
        if(gameBoard.readBoard(0,0)==0):
            moveToReturn[0]=0
            moveToReturn[1]=0
        elif(gameBoard.readBoard(0,2)==0):
            moveToReturn[0]=0
            moveToReturn[1]=2
        elif(gameBoard.readBoard(2,0)==0):
            moveToReturn[0]=2
            moveToReturn[1]=0
        elif(gameBoard.readBoard(0,2)==0):
            moveToReturn[0]=0
            moveToReturn[1]=2
        #If no corner was found, assign the last available space
        else:
            moveToReturn[0] = lastAvailableFreeSpace[0]
            moveToReturn[1] = lastAvailableFreeSpace[1]
            
    #Return Move
    return moveToReturn
    
    
               
#Main Function. Procedure for playing a game. Ties together Board, AI, and user input. 
if __name__ == '__main__':
    pass
    