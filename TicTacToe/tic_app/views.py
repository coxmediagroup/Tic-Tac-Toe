from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from tic_app.Player import AIAgent
from django.http.response import HttpResponse
from django.utils import simplejson
import random

# Create your views here.

legal_first_moves = (0,2,4,6,8)

# index view 

@csrf_exempt
def index  (request):
    if(random.randint(0,1)==0):
        first_move = random.choice(legal_first_moves)
        return render(request,'tic_app/index.html',{'first_move':first_move})
    else:
         return render(request,'tic_app/index.html')

# take a request containing the state of game and returns with ajax response the next move to the game
@csrf_exempt
def process_state_ajax(request):
    if request.method=="POST" and request.is_ajax() and request.POST.has_key('info[]'):
        win = 'false'
        tie = 'false'
        response_dict = {}
        game_state = request.POST.getlist('info[]')
        if game_state is not None:
            (next_move,win) = AIAgent(game_state,'o').next_move(game_state);
            if win==1:
                win='true'
            response_dict.update({'next_move':chr(int(next_move)+97).upper()})
            response_dict.update({'win':win})
            response_dict.update({'tie':tie})
        return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')
    else:
        return render(request,'tic_app/index.html')

# reinitialize the game (when user click playAgain button)
@csrf_exempt
def first_move_ajax(request):
    response_dict ={}
    if request.method=="POST" and request.is_ajax():
       if(random.randint(0,1)==0):
           first_move = random.choice(legal_first_moves) 
           response_dict.update({'first_move':chr(random.choice(legal_first_moves)+97).upper()})
       return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')
           
    else:
        return render(request,'tic_app/index.html')

