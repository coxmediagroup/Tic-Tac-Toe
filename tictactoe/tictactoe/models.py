from django.db import models
from django.contrib import admin

class Game(models.Model):
    player_id = models.TextField(unique=True)
    board = []
    
    def newBoard(self):
        self.board = []
        for i in range(9):
            self.board.append(0)
            
    def addPlay(self, space, play):
        if self.spaceAvailable(space):
            self.board[space] = play
            return True
        else:
            return False
    
    def spaceAvailable(self, space):
        return self.board[space] is 0
    
    def isWin(self):
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
            if len(set(self.board[i*3:i*3+3])) is  1 and self.board[i*3] is not 0: return True
        ### check if any of the Columns has winning combination
        for i in range(3):
           if (self.board[i] is self.board[i+3]) and (self.board[i] is  self.board[i+6]) and self.board[i] is not 0:
               return True
        ### 2,4,6 and 0,4,8 cases
        if self.board[0] is self.board[4] and self.board[4] is self.board[8] and self.board[4] is not 0:
            return  True
        if self.board[2] is self.board[4] and self.board[4] is self.board[6] and self.board[4] is not 0:
            return  True
        return False

    def nextMove(self, player):
        """
        source: https://gist.github.com/SudhagarS/3942029
        Computes the next move for a player given the current board state and also
        computes if the player will win or not.
     
        Arguments:
            board: list containing X,- and O
            player: one character string 'X' or 'O'
     
        Return Value:
            willwin: 1 if 'X' is in winning state, 0 if the game is draw and -1 if 'O' is
                        winning
            nextmove: position where the player can play the next move so that the
                             player wins or draws or delays the loss
        """
        ### when board is '---------' evaluating next move takes some time since
        ### the tree has 9! nodes. But it is clear in that state, the result is a draw
        if len(set(self.board)) == 1: return 0,4
     
        nextplayer = 2 if player==1 else 1
        if self.isWin() :
            if player is 2: return -1,-1
            else: return 1,-1
        res_list=[] # list for appending the result
        c= self.board.count(0)
        if  c is 0:
            return 0,-1
        _list=[] # list for storing the indexes where 0 appears
        for i in range(len(self.board)):
            if self.board[i] == 0:
                _list.append(i)
        #tempboardlist=list(board)
        for i in _list:
            self.board[i]=player
            ret,move=self.nextMove(nextplayer)
            res_list.append(ret)
            self.board[i]=0
        if player is 2:
            maxele=max(res_list)
            return maxele,_list[res_list.index(maxele)]
        else :
            minele=min(res_list)
            return minele,_list[res_list.index(minele)]
        
    def printPlays(self):
        for i in range(len(self.board)):
            print self.board[i]
            
class GameAdmin(admin.ModelAdmin):
    pass

class Play(models.Model):
    OPIECE = 1
    XPIECE = 2
    
    game = models.ForeignKey(Game, related_name="plays")
    space = models.IntegerField()
    play = models.IntegerField(default=0)

class PlayAdmin(admin.ModelAdmin):
    list_display = ["game"]
    
admin.site.register(Play, PlayAdmin)
admin.site.register(Game, GameAdmin)