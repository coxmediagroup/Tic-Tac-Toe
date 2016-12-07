from django.db import models
from django.contrib import admin
import json

class Board(models.Model):
    player_id = models.TextField(unique=True)
    cell0 = models.IntegerField(default=0)
    cell1 = models.IntegerField(default=0)
    cell2 = models.IntegerField(default=0)
    cell3 = models.IntegerField(default=0)
    cell4 = models.IntegerField(default=0)
    cell5 = models.IntegerField(default=0)
    cell6 = models.IntegerField(default=0)
    cell7 = models.IntegerField(default=0)
    cell8 = models.IntegerField(default=0)
    playCount = models.IntegerField(default=0)

    def __str__(self):
        return self.player_id
    
    def __json__(self):
        ret_value = {"board":self.board, "isWin":self.isWin(self.board), 'isTie':self.isTie(), 'playCount':self.playCount}
        return json.dumps(ret_value)
        
    @property
    def board(self):
        return [self.cell0,self.cell1,self.cell2,
                self.cell3,self.cell4,self.cell5,
                self.cell6,self.cell7,self.cell8]
    
    def newBoard(self):
        self.playCount = 0
        self.cell0 = self.cell1 = self.cell2 = self.cell3 = self.cell4 = self.cell5 = self.cell6 = self.cell7 = self.cell8 = 0
        self.save()
            
    def addPlay(self, space, play):
        #find the right cell, update the model and ignore out of bounds requests.
        #returns true if the space is open and if the play was made
        if self.spaceAvailable(space):
            if space in range(9):
                self.playCount = self.playCount+1
                
            if space==0:
                self.cell0 = play
            elif space==1:
                self.cell1 = play
            elif space==2:
                self.cell2 = play
            elif space==3:
                self.cell3 = play
            elif space==4:
                self.cell4 = play
            elif space==5:
                self.cell5 = play
            elif space==6:
                self.cell6 = play
            elif space==7:
                self.cell7 = play
            elif space==8:
                self.cell8 = play
            
            self.save()
            return True
        else:
            return False
    
    def spaceAvailable(self, space):
        if space in range(9):
            return self.board[space] is 0
        else:
            return False
    
    def isTie(self):
        if not self.isWin(self.board):
            return (self.board.count(1) + self.board.count(2)) >= 8
        else:
            return False
    
    def isWin(self, board):
        """
        source: https://gist.github.com/SudhagarS/3942029
        
        Given a board checks if it is in a winning state.
        Arguments:
              board: a list containing 0,1 or 2.
        Return Value:
               True if board in winning state. Else False
        """
        ### check if any of the rows has winning combination
        for i in range(3):
            if len(set(board[i*3:i*3+3])) is  1 and board[i*3] is not 0: return True
        ### check if any of the Columns has winning combination
        for i in range(3):
           if (board[i] is board[i+3]) and (board[i] is  board[i+6]) and board[i] is not 0:
               return True
        ### 2,4,6 and 0,4,8 cases
        if board[0] is board[4] and board[4] is board[8] and board[4] is not 0:
            return  True
        if board[2] is board[4] and board[4] is board[6] and board[4] is not 0:
            return  True
        return False

    def nextMove(self, board, player):
        """
        source: https://gist.github.com/SudhagarS/3942029
        Computes the next move for a player given the current board state and also
        computes if the player will win or not.
     
        Arguments:
            board: list containing 2(X),0(-) and (1)O
            player: one character string 2('X') or (1)'O'
     
        Return Value:
            willwin: 1 if 'X' is in winning state, 0 if the game is draw and -1 if 'O' is
                        winning
            nextmove: position where the player can play the next move so that the
                             player wins or draws or delays the loss
        """
        ### when board is '---------' evaluating next move takes some time since
        ### the tree has 9! nodes. But it is clear in that state, the result is a draw
        
        if len(set(board)) == 1: return 0,4
        
        nextplayer = 2 if player==1 else 1
        if self.isWin(board) :
            if player is 2: return -1,-1
            else: return 1,-1
        res_list=[] # list for appending the result
        c= board.count(0)
        if  c is 0:
            return 0,-1
        _list=[] # list for storing the indexes where 0 appears
        for i in range(len(board)):
            if board[i] == 0:
                _list.append(i)
        #tempboardlist=list(board)
        for i in _list:
            board[i]=player
            ret,move=self.nextMove(board, nextplayer)
            res_list.append(ret)
            board[i]=0
        if player is 2:
            maxele=max(res_list)
            return maxele,_list[res_list.index(maxele)]
        else :
            minele=min(res_list)
            return minele,_list[res_list.index(minele)]
    
    def computerPlay(self):
        #create a copy of board in memory
        board = self.board
        willWin, nextMove = self.nextMove(board, 2)
        self.addPlay(nextMove, 2)
        
    def printBoard(self):
        if self.isWin(self.board):
            print "Game Over"
        elif self.isTie():
            print "Game Tied"
            
        for i in range(3):
            for j in range(3):
                if self.board[i*3+j]==2:
                    print "X",
                elif self.board[i*3+j]==1:
                    print "O",
                else:
                    print "-",
            print ""