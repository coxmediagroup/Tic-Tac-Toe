from django.http import *
from main.models import *
from django.template import Context, loader
from ttt_lib import *
import pickle

#set host ip or hostname
host="localhost"


def game(request, game_id=1):
    
    #render game board
    
    gameSession = Games.objects.get_or_create(id=game_id)
    gameSession[0].save()
    
    gameSession = gameSession[0]

    
    
    game_template = loader.get_template('main/board.html')
    
    spaces = pickle.loads(str(gameSession.board.spaceStateList))
    
    #send board space states and game id to user
    game_context = Context({'rows': spaces, 'winner': "none", 'game_session_id': gameSession.id, })
    
    return HttpResponse(game_template.render(game_context))
    
def reqNewGame(request):
    
    
    return HttpResponseRedirect("/game/"+str(newGame())+"/")
    
    
    
def listGames(request):
    pass
    # query to get all game objects
    
def reqMove(request, game_id, move):
    
    webMove(game_id, move)
    
    return HttpResponseRedirect("/game/"+game_id+"/")
