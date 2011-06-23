from django.http import HttpResponse
import json

def newgame(request, xo):
    if xo not in ('x','o'):
        response = {
            'success': False,
            'message': 'Please set player to either X or O.'
        }
    else:
        response = {
            'success': True,
            'message': 'Player set to '+xo
        }
    
    return HttpResponse(json.dumps(response), mimetype="application/json")

def makemove(request, x, y):
    # check if spot is already taken
    # yes? return error
    # no? place mark, save in session, and check for win
    return HttpResponse(json.dumps({'success':False,'message':'Not yet implemented.'}), mimetype="application/json")

def getmove(request):
    # calculate next move based on session data
    # place mark, save in session, and check for win
    return HttpResponse(json.dumps({'success':False,'message':'Not yet implemented.'}), mimetype="application/json")