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
