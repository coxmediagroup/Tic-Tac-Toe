import logging
from django.db import models
from picklefield.fields import PickledObjectField

class TicTacToeModel(models.Model):
    gameID = models.AutoField(primary_key=True)
    sessionID = models.CharField(max_length=255, help_text="Used to prevent the user from affecting other games by form editing.")
    playerCharacter = models.CharField(max_length=1, help_text="Determines if they are X or O.")
    cpuCharacter = models.CharField(max_length=1)
    boardSize = models.IntegerField()
    gameBoard = PickledObjectField()
    winner = ' '

    def putPlayerMove(self,row,col):
        '''Set the player move'''
        self.gameBoard[row][col] = self.playerCharacter

    def putCPUMove(self,row,col):
        '''Set the cpu move'''
        self.gameBoard[row][col] = self.cpuCharacter

    def clearMove(self,row,col):
        '''Clear the current place on the board'''
        self.gameBoard[row][col] = ' '

    def calculateCPUMove(self):
        '''Calculate and do the CPU Move'''
        move_position, score = self.getMaximizedMove()
        self.putCPUMove(move_position[0], move_position[1])

    def getMaximizedMove(self):
        ''' Find maximized move'''
        bestScore = None
        bestMove = None

        for row_index, row_value in enumerate(self.gameBoard):
            for column_index, column_value in enumerate(row_value):
                if column_value == ' ':
                    #Mark the position as now taken by the CPU
                    self.putCPUMove(row_index, column_index)

                    #Check opponent move possibilities
                    if self.checkGameOver():
                        score = self.calculateScore()
                    else:
                        move_position,score = self.getMinimizedMove()

                    #Revert back from the move
                    self.clearMove(row_index, column_index)

                    if bestScore == None or score > bestScore:
                        bestScore = score
                        bestMove = [row_index, column_index]

        return bestMove, bestScore

    def getMinimizedMove(self):
        ''' Find minimized move'''

        bestScore = None
        bestMove = None
        for row_index, row_value in enumerate(self.gameBoard):
            for column_index, column_value in enumerate(row_value):
                if column_value == ' ':
                    self.putPlayerMove(row_index, column_index)

                    if self.checkGameOver():
                        score = self.calculateScore()
                    else:
                        move_position,score = self.getMaximizedMove()

                    #Revert back from the move
                    self.clearMove(row_index, column_index)

                    if bestScore == None or score < bestScore:
                        bestScore = score
                        bestMove = [row_index, column_index]

        return bestMove, bestScore

    def checkGameOver(self):
        '''Check to see if we have a winner'''
        for row_index, row_value in enumerate(self.gameBoard):

            #Check for a horizontal winner
            if row_value.count(' ') == 0:
                self.winner = row_value[0]
                return True

            #Other win conditions later
        return False

    def calculateScore(self):
        '''Get the score of the result'''
        if self.checkGameOver():
            if self.winner  == self.cpuCharacter:
                return 1 # CPU Won
            elif self.winner == self.playerCharacter:
                return -1 # Person won
        return 0 # Draw








