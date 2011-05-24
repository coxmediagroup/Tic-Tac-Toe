from django.db import models
from tic_tac_toe import *
#from main import  *
from ttt_lib import *
import pickle




class Boards(models.Model):
        
    spaceStateList = models.TextField()
    optimalMoves = models.TextField()
    
    
    
class Games(models.Model):

    gameDate = models.DateField(auto_now=True)
    lastMoved = models.DateField(auto_now=True)
    gameOver = models.BooleanField()
    board = models.ForeignKey(Boards, default=1)
        
def newGame():

    
    newBoard = Boards.objects.get_or_create(spaceStateList=pickle.dumps([' ',' ',' ',' ',' ',' ',' ',' ',' ']))
    newBoard[0].save()
    gameSession = Games()
    gameSession.board = newBoard[0]
    gameSession.save()
    
    return gameSession.id

def webMove(game_id, move):
    
    #look up game
    gameSession = Games.objects.get(id=int(game_id))
    
    
    #make move
    gameSim= TicTacToeBoard()
    gameSim.board_space = pickle.loads(str(gameSession.board.spaceStateList))
    
    #check if move is possible
    if gameSim.board_space[int(move)] != ' ':
        
        return False
    if gameSim.gameOver():
        gameSession.gameOver=True
        gameSession.save()
        return False
        
    #make move for player
    gameSim.board_space[int(move)] = 'X'
    nextBoard = Boards.objects.get_or_create(spaceStateList=pickle.dumps(gameSim.board_space))
    nextBoard = nextBoard[0]
    nextBoard.save()
    gameSession.board = nextBoard
    gameSession.save()
    if gameSim.gameOver():
        gameSession.gameOver=True
        return False

    #look up optimal moves for cpu ('X')
    optmove = gameSession.board.optimalMoves
    if optmove: optmove=pickle.loads(str(optmove))
    
    if optmove:
        gameSim.board_space[optmove[-1][0]] = "O"
        nextBoard = Boards.objects.get_or_create(spaceStateList=pickle.dumps(gameSim.board_space))
        nextBoard = nextBoard[0]
        nextBoard.save()
        gameSession.board = nextBoard
        gameSession.save()
    else:
        
        computerPlayer(gameSim, "O")
        gameSession.board.optimalMoves = pickle.dumps(gameSim.optmoves)
        gameSession.board.save()
        gameSession.save()
        gameSim.board_space[gameSim.optmoves[-1][0]] = "O"
        nextBoard = Boards.objects.get_or_create(spaceStateList=pickle.dumps(gameSim.board_space))
        nextBoard[0].save()
        gameSession.board = nextBoard[0]
        gameSession.save()
    
    return True
                                