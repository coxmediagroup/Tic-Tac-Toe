# project imports
from models import TicTacToeGame
import computer_logic as cl

# library imports
import simplejson

# django support imports
from django.middleware.csrf import get_token
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext


def home(request):
    """Render home page."""
    return render_to_response('home.html', {},
        context_instance = RequestContext(request))

def play(request):
    """Create new TicTacToeGame and render play page."""
    ttt = TicTacToeGame()
    ttt.save()
    return render_to_response('play.html', {'game_id':ttt.id},
        context_instance = RequestContext(request))

def about(request):
    """Render about page."""
    return render_to_response('about.html', {},
        context_instance = RequestContext(request))

def human_play(request, game, cell):
    """Handle human playing on board."""
    r, c = cell.split('_')[1:]
    next_pos = ( int(r), int(c) )
    ttt = TicTacToeGame.objects.get(id=int(game))
    ttt.update_board(2, next_pos)
    ttt.save()
    end_of_game = ttt.open_cell_count() == 0
    print 'end of game', ttt.open_cell_count(), end_of_game
    return HttpResponse(simplejson.dumps({'next_pos': next_pos,
                                          'end_of_game': end_of_game,
                                          'board': ttt.get_board()}))

def computer_play(request, game):
    """Handle computer play, including executing logic to
    determine the next best move."""
    ttt = TicTacToeGame.objects.get(id=int(game))
    next_pos, win_move = cl.next_move(ttt)
    ttt.update_board(1, next_pos)
    ttt.print_board()
    ttt.save()
    end_of_game = ttt.open_cell_count() == 0
    print 'end of game', ttt.open_cell_count(), end_of_game
    return HttpResponse(simplejson.dumps({'next_pos': next_pos,
                                          'win_move': win_move,
                                          'end_of_game': end_of_game,
                                          'board': ttt.get_board()}))

def update_challenger(request, game, name):
    """CURRENTLY UNUSED.
    Update the challenger name field in the database.
    Future work could let a user change his/her name
    allowing for a "leader board" to show who lost vs
    who tied the computer."""
    ttt = TicTacToeGame.objects.get(id=int(game))
    ttt.player = name
    ttt.save()
    return HttpResponse(200)
