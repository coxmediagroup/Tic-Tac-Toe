# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from tictactoe_django.game.object import TicTacToe

import simplejson

game = TicTacToe()

def index(request, template='index.html'):
    game.__init__()
    
    variables = RequestContext(request, {
        'layout': game.layout,
    })
    return render_to_response(template, variables)

def set_challenger(request):
    
    if request.is_ajax():
        result = {}
        
        if game.challenger:
            result.update(dict(
                error='You are already playing as ' + game.challenger
            ))

        else:
            game.challenger = request.POST.get('challenger')
            game.computer = [i for i in game.players if i != game.challenger][0]
            
            if game.challenger_path == game.computer_path and \
                game.challenger == 'O':
                computer_move = game.counter_move(game.computer)
                
                result.update(dict(
                    counter=dict(sign=game.computer, pos=computer_move)
                ))
        json = simplejson.dumps(result)
        return HttpResponse(json, mimetype='application/json')


def play(request):
    
    if request.is_ajax() and game.finished == False:
        new_pos = int(request.POST.get('pos'))
        result = {}
        
        if not game.challenger:
            result.update(dict(error='You have to choose whether you want to play as "X" or "O"'))
            json = simplejson.dumps(result)
            return HttpResponse(json, mimetype='application/json')
        
        challenger_move = game.make_a_move(new_pos, game.challenger)
        computer_move = game.counter_move(game.computer)

        result.update(dict(move=dict(sign=game.challenger,
                                           pos=challenger_move)))
        result.update(dict(counter=dict(sign=game.computer, pos=computer_move)
        ))
                
        if game.finished:
            winner = game.who_wins()
            
            if winner == game.challenger:
                message = 'You won.'
            
            elif winner == game.computer:
                message = 'You lost.'
            else:
                message = 'Draw.'
            result.update(dict(finish_message=message))

        
        # result.update(dict(
        #     winner=game.who_wins()
        # ))
        
        json = simplejson.dumps(result)
        return HttpResponse(json, mimetype='application/json')
        