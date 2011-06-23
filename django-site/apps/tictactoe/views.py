from django.http import HttpResponse
import json, random

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
    x = int(x)
    y = int(y)
    matrix = request.session['matrix'];
    if matrix[x][y]:
        response = {
            'success': False,
            'message': 'Invalid move: spot already taken.'
        }
    else:
        matrix[x][y] = 1
        request.session['matrix'] = matrix
        response = {
            'success': True
        }
    return HttpResponse(json.dumps(response), mimetype="application/json")

def getmove(request):
    # calculate next move based on session data
    matrix = request.session['matrix'];
    #right now just random
    while True:
        x = random.randint(0,2);
        y = random.randint(0,2);
        if matrix[x][y] == 0:
            matrix[x][y] = 2;
            response = {
                'success': True,
                'x': x,
                'y': y
            }
            break;
    
    # place mark, save in session, and check for win
    return HttpResponse(json.dumps(response), mimetype="application/json")