from django.shortcuts import render
from tictactoe.game import forms as gameforms
from tictactoe.game.models import TicTacToeModel
from tictactoe.responses import HttpResponseSeeOtherRedirect

from django.core.urlresolvers import reverse



def index(request):
    '''This is the initial view that lists the few navigation options that this
    application supports.
    '''
    sizeForm = gameforms.BoardSizeForm(initial={'boardSize': 3})
    return render(request, 'game/index.html', {'sizeForm': sizeForm})

def createGame(request):
    '''This is the view that sets up the actual game board.
    '''
    if(request.method == 'POST'):
        sizeForm = gameforms.BoardSizeForm(request.POST)
        if sizeForm.is_valid():
            boardSize = int(request.POST['boardSize'])

            game = TicTacToeModel.objects.create(
                boardSize = boardSize,
                gameBoard = [[' '] * boardSize,] * boardSize,
                playerCharacter = request.POST['playerCharacter'],
                sessionID = request.session.session_key
            )
            game.save()

            gameForm = gameforms.TicTacToeForm(initial={'gameID': game.gameID})

            return render(request, 'game/playGame.html', {'gameObj': game, 'gameForm': gameForm, 'sizeForm': sizeForm})

    return HttpResponseSeeOtherRedirect(reverse('site-index'))

def doMove(request):
    '''This is the initial view placeholder for the game itself.
    '''

    if(request.method == 'POST' and gameforms.TicTacToeForm(request.POST).is_valid()):
        game = TicTacToeModel(gameID=request.POST["gameID"], sessionID=request.session.session_key)
        gameForm = gameforms.TicTacToeForm(initial={'gameID': game.gameID})
        game.save()
        return render(request, 'game/playGame.html', {'gameObj': game, 'gameForm': gameForm})