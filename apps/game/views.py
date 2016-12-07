from random import randint
import json
import time

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse

from game.models import Game

def home(request):
    '''Renders main application page. Loads prior game in progress if one exists, otherwise loads blank board.
    '''
    if request.session.get('has_game', False):
        g = Game.objects.filter(session_id=request.session._session_key).order_by('-date_created')[0]
        board = g.get_board()
        board = [i if i is not None else '' for i in board]
        player_human = g.player_human
    else:
        board = []
        player_human = ''
    return render_to_response('game/home.html',
                              {'board': board,
                               'has_game': request.session.get('has_game', ''),
                               'player_human': player_human},
                               context_instance=RequestContext(request))

def setup(request):
    '''AJAX function for creating new game.
    '''
    if not request.is_ajax():
        return HttpResponse('Invalid call. AJAX required.')

    player_human = request.POST['player_human']
    player_AI = None
    if player_human == 'X':
        player_AI = 'O'
    else:
        player_AI = 'X'

    g = Game(session_id=request.session._session_key, player_human=player_human, player_AI=player_AI)
    g.save()
    request.session['has_game'] = True
    return HttpResponse('Game created.')


def play(request):
    '''AJAX function that contains main game flow logic. Checks for win/tie after the human player's move. Then chooses a move for the AI player and checks again for win/tie. Clears session and returns a JSON response whenever a win/tie is detected.
    '''
    if not request.is_ajax():
        return HttpResponse('Invalid call. AJAX required.')

    time.sleep(1)
    space_human = int(request.POST['space_human'])

    # retrieve game from database (the most recent one saved under user's session id)
    g = Game.objects.filter(session_id=request.session._session_key).order_by('-date_created')[0]

    player_human = g.player_human
    player_AI = g.player_AI

    g.make_move(player_human, space_human)

    if g.get_winner():
        g.winner = g.get_winner()
        g.save()
        response = ({'winner': player_human,
                     'tie': True
                    })
        request.session.flush()
        return HttpResponse(json.dumps(response), content_type="application/json")

    if g.is_tie():
        g.winner = 'cat'
        g.save()
        response = ({'winner': 'the cat',
                     'tie': True
                    })
        request.session.flush()
        return HttpResponse(json.dumps(response), content_type="application/json")

    # decide AI's move
    winning_moves = g.get_winning_moves()
    fork_moves = g.get_fork_moves()
    possible_moves = g.get_possible_moves()
    possible_corner_moves = list(set([0,2,6,8]) & set(possible_moves))
    possible_side_moves = list(set([1,3,5,7]) & set(possible_moves))

    if winning_moves[player_AI]: # win if possible
        space_AI = winning_moves[player_AI][0] # there should only be one item in the list unless someone has missed an opportunity
    elif winning_moves[player_human]: # block human win
        space_AI = winning_moves[player_human][0]
    elif fork_moves[player_AI]: # make a move that would result in a fork (guaranteed win on next turn)
        space_AI = fork_moves[player_AI][0]
    elif len(fork_moves[player_human]) == 1: # block the opponent's fork
        space_AI = fork_moves[player_human][0]
    elif len(fork_moves[player_human]) > 1: # 2 possible forks; force opponent to block AI win on next turn
        space_AI = possible_side_moves[randint(0,len(possible_side_moves)-1)]
    elif 4 in possible_moves: # play center
        space_AI = 4
    elif possible_corner_moves: # play corner
        space_AI = possible_corner_moves[randint(0,len(possible_corner_moves)-1)]
    elif possible_side_moves: # play side
        space_AI = possible_side_moves[randint(0,len(possible_side_moves)-1)]
    else: # error
        return HttpResponse(json.dumps({'error': "hit impossible condition...apparently it wasn't impossible after all!"}), content_type="application/json")

    g.make_move(player_AI, space_AI)

    if g.get_winner():
        g.winner = g.get_winner()
        g.save()
        response = ({'space_AI': str(space_AI),
                     'winner': player_AI,
                     'tie': False,
                     'player_AI': player_AI,
                     'player_human': player_human
                   })
        request.session.flush()
        return HttpResponse(json.dumps(response), content_type="application/json")

    if g.is_tie():
        g.winner = 'cat'
        g.save()
        response = ({'space_AI': str(space_AI),
                     'winner': 'the cat',
                     'tie': True,
                     'player_AI': player_AI,
                     'player_human': player_human
                   })
        request.session.flush()
        return HttpResponse(json.dumps(response), content_type="application/json")

    response = ({'space_AI': str(space_AI),
                 'player_AI': player_AI,
                 'player_human': player_human
                })
    return HttpResponse(json.dumps(response), content_type="application/json")

def thanks(request):
    '''Renders simple thank you page after user decides to play no more.
    '''
    return render_to_response('game/thanks.html')

def clear(request):
    '''AJAX function to clear session after game is over.
    '''
    if not request.is_ajax():
        return HttpResponse('Invalid call. AJAX required.')
    request.session.flush()
    return HttpResponse('Session cleared.')