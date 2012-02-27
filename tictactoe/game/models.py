import logging
from django.db import models
from picklefield.fields import PickledObjectField

class TicTacToeModel(models.Model):
    gameID = models.AutoField(primary_key=True)
    sessionID = models.CharField(max_length=255, help_text="Used to prevent the user from affecting other games by form editing.")
    playerCharacter = models.CharField(max_length=1, help_text="Determines if the player is X or O.")
    cpuCharacter = models.CharField(max_length=1, help_text="The side that the CPU is on (X or O).")
    boardSize = models.IntegerField(help_text="Length and width of the square board.")
    gameBoard = PickledObjectField()

    #Winner of the game
    winner = ' '

    #maximum number of moves to look forward as it gets CPU intensive
    maximum_move_depth = 0
    current_move_depth = 0


    def putPlayerMove(self,row,col):
        '''Set the player move'''
        if self.gameBoard[row][col] == ' ':
            self.gameBoard[row][col] = self.playerCharacter

    def putCPUMove(self,row,col):
        '''Set the cpu move'''
        self.gameBoard[row][col] = self.cpuCharacter

    def clearMove(self,row,col):
        '''Clear the current place on the board'''
        self.gameBoard[row][col] = ' '

    def calculateCPUMove(self):
        '''Calculate and do the CPU Move'''

        #Set the maximum number of expected moves  the system can handle.
        self.current_move_depth = 0
        if self.getOpenSpacesCount() < 9:
            self.maximum_move_depth = 7
        elif self.getOpenSpacesCount() < 13:
            self.maximum_move_depth = 5
        elif self.getOpenSpacesCount() < 23:
            self.maximum_move_depth = 4
        elif self.getOpenSpacesCount() < 50:
            self.maximum_move_depth = 3
        else:
            self.maximum_move_depth = 2

        if not self.checkGameOver():
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
                    self.current_move_depth += 1

                    #Check opponent move possibilities
                    if self.checkGameOver() or self.current_move_depth >= self.maximum_move_depth:
                        score = self.calculateScore()
                    else:
                        move_position,score = self.getMinimizedMove()

                    #Revert back from the move
                    self.clearMove(row_index, column_index)
                    self.current_move_depth -= 1

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
                    self.current_move_depth += 1

                    if self.checkGameOver() or self.current_move_depth >= self.maximum_move_depth:
                        score = self.calculateScore()
                    else:
                        move_position,score = self.getMaximizedMove()

                    #Revert back from the move
                    self.clearMove(row_index, column_index)
                    self.current_move_depth -= 1

                    if bestScore == None or score < bestScore:
                        bestScore = score
                        bestMove = [row_index, column_index]

        return bestMove, bestScore

    def checkGameOver(self):
        '''Check to see if we have a winner'''

        #Check for a horizontal winner
        for row_values in self.gameBoard:
            if row_values.count(self.playerCharacter) == self.boardSize or row_values.count(self.cpuCharacter) == self.boardSize:
                self.winner = row_values[0]
                return True

        #Check for a verticle winner
        for column_values in zip(*self.gameBoard):
            #FIXME: Transposing a character onto a blank space leaves the extra space in the list which makes this slightly uglier.
            if (column_values.count(self.playerCharacter) + column_values.count(' '+self.playerCharacter)) == self.boardSize or (column_values.count(self.cpuCharacter) + column_values.count(' '+self.cpuCharacter)) == self.boardSize:
                self.winner = column_values[0]
                return True

        #Check for a diagonal winner - top left to bottom right
        winner_found = True
        column_index = 0
        starting_character_val = self.gameBoard[0][column_index]
        for row_values in self.gameBoard:
            if row_values[column_index] == ' ' or starting_character_val != row_values[column_index]:
                winner_found = False
                break
            column_index+=1

        if(winner_found):
            self.winner = starting_character_val
            return True

        #Check for a diagonal winner - top right to bottom left
        winner_found = True
        column_index = self.boardSize-1
        starting_character_val = self.gameBoard[0][column_index]
        for row_values in self.gameBoard:
            if row_values[column_index] == ' ' or starting_character_val != row_values[column_index]:
                winner_found = False
                break
            column_index-=1

        if(winner_found):
            self.winner = starting_character_val
            return True

        #Finally, check for a draw game with no moves
        space_found = False
        for row_values in self.gameBoard:
            if row_values.count(' ') != 0:
                space_found = True
                break

        if(not space_found):
            self.winner = ' '
            return True

        return False

    def calculateScore(self):
        '''Get the score of the result'''
        if self.checkGameOver():
            if self.winner  == self.cpuCharacter:
                return 1 # CPU Won
            elif self.winner == self.playerCharacter:
                return -1 # Person won
        return 0 # Draw

    def getOpenSpacesCount(self):
        '''Get the total amount of open spaces'''
        count = 0
        for row_values in self.gameBoard:
            count += row_values.count(' ')

        return count








