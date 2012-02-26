import logging
import os
from django.shortcuts import render
from tictactoe.game import forms as gameforms
from tictactoe.game.models import TicTacToeModel


def index(request):
    '''This is the initial view that lists the few navigation options that this
    application supports.
    '''
    return render(request, 'game/index.html')

def playGame(request, playerCharacter='X'):
    '''This is the initial view placeholder for the game itself.
    '''

    if(request.method == 'POST' and gameforms.TicTacToeForm(request.POST).is_valid()):
        game = TicTacToeModel(gameID=request.POST["gameID"], sessionID=request.session.session_key)
    else:
        game = TicTacToeModel.objects.create(sessionID=request.session.session_key, playerCharacter=playerCharacter)

    #if request.method == 'POST' and gameforms.TicTacToeForm(request.POST).is_valid():
        #Add logic for game here.

    form = gameforms.TicTacToeForm(initial={'gameID': game.gameID})
    game.save()

    return render(request, 'game/playGame.html', {'gameObj': game, 'form': form})