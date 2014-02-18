# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from tictactoe.tictactoe import Board
from tictactoe.tictactoe import AIPlayer
import simplejson
def home(request):
    """
        This view will return an html string to be rendered in the template representing the state of the game
        so that the view only ever renders one tic tac toe game at the time
    """
    # here we need to parse out the current state of the board so we can pass it to the class and render it

    try:
        board = simplejson.loads(str(request.GET['board']))

    except:
        board = ['','','','','X','','','','']

    if request.GET['board']:




        ai = AIPlayer('X')

        board.look_for_win(the_board,ai)

    else:
        the_board = Board(the_board=board)
        board_html = the_board.draw()
    return render_to_response('play/home.html',locals())