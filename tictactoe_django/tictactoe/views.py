from django.shortcuts import *
import simplejson

def home(request):
    """ Shows main board for current session. """
    reset_gamestate(request)
    board = simplejson.dumps(request.session['gamestate'].board)
    return render(request, 'home.django.html', {'board': board})

def playeraction(request):
    if make_player_move(request.session['gamestate'], request.POST['pos']):
        if not request.session['gamestate'].check_for_winner():
            make_ai_move(request.session['gamestate'])
        request.session.modified = True
    return HttpResponse(request.session['gamestate'].get_json(),
                        mimetype="application/json")

from functions import *