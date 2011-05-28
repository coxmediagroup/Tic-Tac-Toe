import logic
import pickle
from functools import wraps
from django.shortcuts import render_to_response

def get_board(f):
    """
    Gets the board data from the session and auto-appends it to the argument list 
    of the view
    """
    @wraps(f)
    def newf(request, *args, **kwargs):
        if request.session.get('game', None):
            args = pickle.loads(request.session['game'])
            board = logic.Board(*args)
        else:
            board = logic.Board()
        kwargs['board'] = board
        return f(request, *args, **kwargs)
    return newf
        

@get_board
def index(request, board):
    return render_to_response('base.html')x

           

