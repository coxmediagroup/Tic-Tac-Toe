# from ttt.models import TicTacToe
# import simplejson

from django.middleware.csrf import get_token
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext


def home(request):
    return render_to_response('home.html', {},
        context_instance = RequestContext(request))

# def signin(request):
#     return render_to_response('signin.html', {},
#        context_instance = RequestContext(request))


def play(request):
    return render_to_response('play.html', {},
        context_instance = RequestContext(request))

def update_challenger(request, game, name):
    print 'game', game
    print 'name', name
    return HttpResponse(200)

# def mark_square(request, game, player, row, col):
    # ttt = TicTacToe.objects.get(id=game)
    # ttt.update_board(player, (row, col))
    # return HttpResponse(simplejson.dumps({'board':ttt.get_board()}), 
    #                     mimetype="application/json")

