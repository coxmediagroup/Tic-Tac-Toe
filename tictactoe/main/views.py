import json
from django.http import HttpResponse
from django.template import Context, loader
from collections import Counter
from gamelogic import isWin, nextMove

def index(request):
    template = loader.get_template('main/index.html')
    context = Context({})
    return HttpResponse(template.render(context))

def getMatrixFromJSON(request):
    """
    Pass request object and return a 9 member list, representing our game board matrix.
    """
    matrixList = []

    # using Python json encoder/decoder, but may switch out for Django's simplejson, after I gain familiarity with it.
    JSONParsed = json.loads(request.read())

    # Could have used list comprehension here, but this is more easily read.
    for marker in JSONParsed:
        player = '-' if marker['chosen'] == False else marker['player']
        matrixList.append(player)

    return matrixList
    
def processAJAXRequest(request):
    """
    This handler for calls to /ai. 
    """
    # Initialize a dictionary to hold response vals
    responseDict = {
        'gameOver': False,
        'AIMarker': None,
        'winner': None,
    }

    boardMatrixList = getMatrixFromJSON(request)

    if isWin(boardMatrixList):
        # Human player is grand master of Tic Tac Toe and has won... somehow
        responseDict['gameOver'] = True
        responseDict['winner'] = 'X'
        return HttpResponse(json.dumps(responseDict), content_type='application/json')  

    # Count number of unmarked tiles on board
    if Counter(boardMatrixList)['-'] == 0:
        # Human has taken 9th tile but not won. We've a tie situation on our hands.
        responseDict['gameOver'] = True
        responseDict['winner'] = None
        return HttpResponse(json.dumps(responseDict), content_type='application/json')

    # Player has not won and there is no tie. AI's turn!
    AIMove = nextMove(boardMatrixList,'O')

    responseDict['AIMarker'] = AIMove[1]

    # Insert AI's chosen move into our board matrix and check for AI win.
    boardMatrixList[AIMove[1]] = 'O'
    if isWin(boardMatrixList):
        responseDict['gameOver'] = True
        responseDict['winner'] = 'O'

    return HttpResponse(json.dumps(responseDict), content_type='application/json') 
