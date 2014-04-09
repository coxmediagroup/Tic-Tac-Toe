from ttt.models import TicTacToe
import simplejson

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
    ttt = TicTacToeGame()
    return render_to_response('play.html', {'game_id':ttt.id},
        context_instance = RequestContext(request))

def computer_play(request, game):
    ttt = TicTacToeGame.objects.get(id=int(game))
    next_pos = cl.next_move(ttt)
    ttt.update_board(2, next_pos)
    return HttpResponse(simplejson.dumps({'next_pos': next_pos,
                                           'board': ttt.get_board}))

def update_challenger(request, game, name):
    print 'game', game
    print 'name', name
    return HttpResponse(200)

# def mark_square(request, game, player, row, col):
    # ttt = TicTacToe.objects.get(id=game)
    # ttt.update_board(player, (row, col))
    # return HttpResponse(simplejson.dumps({'board':ttt.get_board()}), 
    #                     mimetype="application/json")

