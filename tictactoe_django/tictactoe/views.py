from django.shortcuts import *
import simplejson

def home(request):
    """ Shows main board for current session. """
    board = simplejson.dumps(request.session['gamestate'].board)
    return render(request, 'home.django.html', {'board': board})

def restart(request):
    reset_gamestate(request)
    return home(request)

def playeraction(request):
    make_player_move(request.session['gamestate'], request.POST['pos'])
    make_ai_move(request.session['gamestate'])
    request.session.modified = True
    return HttpResponse(simplejson.dumps(request.session['gamestate'].board),
                        mimetype="application/json")

from functions import *