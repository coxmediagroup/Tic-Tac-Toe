from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt

from tictactoe.game import forms as gameforms
from tictactoe.game.models import TicTacToeModel
from tictactoe.responses import HttpResponseSeeOtherRedirect

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

            #Setup the game board
            gameBoard = []
            for outer_value in range(0,boardSize):
                inner_loop = []
                for inner_value in range(0,boardSize):
                    inner_loop.append(' ')
                gameBoard.append(inner_loop)

            #Get CPU character
            if request.POST['playerCharacter'] == 'X':
                cpuCharacter = 'O'
            else:
                cpuCharacter = 'X'

            game = TicTacToeModel.objects.create(
                boardSize = boardSize,
                gameBoard = gameBoard,
                playerCharacter = request.POST['playerCharacter'],
                cpuCharacter = cpuCharacter,
                sessionID = request.session.session_key
            )

            if cpuCharacter == 'X':
                game.calculateCPUMove();

            game.save()

            gameForm = gameforms.TicTacToeForm(initial={'gameID': game.gameID})

            return render(request, 'game/playGame.html', {'gameObj': game, 'gameForm': gameForm, 'sizeForm': sizeForm})

    # Redirect to the index if something is wrong. TODO: Add a message about this to the template?
    return HttpResponseSeeOtherRedirect(reverse('site-index'))

@csrf_exempt
def doMove(request):
    '''This is the initial view placeholder for the game itself.
    '''

    if(request.method == 'POST'):
        gameForm = gameforms.TicTacToeForm(request.POST)
        if gameForm.is_valid():

            game = TicTacToeModel.objects.get(gameID=request.POST["gameID"], sessionID=request.session.session_key)
            row, sep, col = request.POST['tictacBoxSelection'].partition(',')
            game.putPlayerMove(int(row), int(col))

            game.calculateCPUMove()

            game.save()

            #If AJAX request, return only the part we need to update. Otherwise fallback and update the whole page.
            if request.is_ajax():
                return render(request, 'game/snippets/tictactoe_board.html', {'gameObj': game})
            else:
                sizeForm = gameforms.BoardSizeForm(initial={'boardSize': game.boardSize, 'playerCharacter':game.playerCharacter})
                return render(request, 'game/playGame.html', {'gameObj': game, 'gameForm': gameForm, 'sizeForm': sizeForm})


    # Redirect to the index if something is wrong. TODO: Add a message about this to the template?
    #return HttpResponseSeeOtherRedirect(reverse('site-index'))