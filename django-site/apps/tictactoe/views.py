from django.http import HttpResponse
import json, random, game

ID_PLAYER = 1
ID_COMPUTER = 2

def newgame(request, xo):
    if xo not in ('x','o'):
        response = {
            'success': False,
            'message': 'Please set player to either X or O.'
        }
    else:
        request.session['matrix'] = [[0,0,0],[0,0,0],[0,0,0]];
        response = {
            'success': True,
            'message': 'Player set to '+xo
        }
    
    return HttpResponse(json.dumps(response), mimetype="application/json")

def makemove(request, x, y):
    # check if spot is already taken
    result = game.makemove(request.session['matrix'], int(x), int(y))
    if result:
        matrix = request.session['matrix']
        matrix[result.x][result.y] = ID_PLAYER
        request.session['matrix'] = matrix
        
        winResult = game.checkforwin(request.session['matrix'])
        
        response = {
            'success': True,
            'win': winResult.win
        }
        if winResult.win:
            response['winner'] = winResult.winnerId
    else:
        response = {
            'success': False,
            'message': 'Invalid move: spot already taken.'
        }
        
    return HttpResponse(json.dumps(response), mimetype="application/json")

def getmove(request):
    result = game.getmove(request.session['matrix'])
    
    if result:
        matrix = request.session['matrix']
        matrix[result.x][result.y] = ID_COMPUTER
        request.session['matrix'] = matrix
        
        winResult = game.checkforwin(request.session['matrix'])
    
        response = {
            'success': True,
            'x': result.x,
            'y': result.y,
            'win': winResult.win
        }
        if winResult.win:
            response['winner'] = winResult.winnerId
    else:
        response = {
            'success': False,
            'message': 'Nowhere to move!'
        }
    
    # place mark, save in session, and check for win
    return HttpResponse(json.dumps(response), mimetype="application/json")