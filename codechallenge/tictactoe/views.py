from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
    return render_to_response('tictactoe/index.html', context_instance=RequestContext(request))

def normal_game(request):
    """ Normal game """
    return render_to_response('tictactoe/game/normal.html', context_instance=RequestContext(request))

def ajax_game(request):
    """ Ajax based game """
    return render_to_response('tictactoe/game/ajax.html', context_instance=RequestContext(request))


