from models import TicTacToeGame
import simplejson

from django.middleware.csrf import get_token
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext


def home(request):
    return render_to_response('home.html', {},
        context_instance = RequestContext(request))

def play(request):
    ttt = TicTacToeGame()
    return render_to_response('play.html', {'game_id':ttt.id},
        context_instance = RequestContext(request))

def human_play(request, game, cell):
    r, c = cell.split('_')[1:]
    next_pos = ( int(r), int(c) )
    ttt = TicTacToeGame.objects.get(id=int(game))
    ttt.update_board(1, next_pos)
    end_of_game = ttt.open_cell_count() == 0
    return HttpResponse(simplejson.dumps({'next_pos': next_pos,
                                          'end_of_game': end_of_game,
                                          'board': ttt.get_board}))

def computer_play(request, game):
    print 'got to computer play'
    print 'game', game
    ttt = TicTacToeGame.objects.get(id=int(game))
    next_pos, win_move = cl.next_move(ttt)
    ttt.update_board(2, next_pos)
    end_of_game = ttt.open_cell_count() == 0
    return HttpResponse(simplejson.dumps({'next_pos': next_pos,
                                          'win_move': win_move,
                                          'end_of_game': end_of_game,
                                          'board': ttt.get_board}))

def update_challenger(request, game, name):
    print 'game', game
    print 'name', name
    ttt = TicTacToeGame.objects.get(id=int(game))
    ttt.player = name
    ttt.save()
    return HttpResponse(200)

def mark_square(request, game, player, row, col):
    ttt = TicTacToeGame.objects.get(id=game)
    ttt.update_board(player, (row, col))
    return HttpResponse(simplejson.dumps({'board':ttt.get_board()}), 
                        mimetype="application/json")

