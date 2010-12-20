# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import serializers
from ttt import plotMove
import json

def ticTacToe(request):
    return render_to_response('ttt/game.html', context_instance=RequestContext(request))
    
    
def ticTacToeMove(request, board, player):
    result = plotMove(board, player)
    next = json.dumps( {"complete" : result[0], "winner" : result[1], "next" : result[2], "nextMarker" : result[3] } )
    return HttpResponse(next, mimetype='application/json')
