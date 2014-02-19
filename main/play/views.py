# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from tictactoe.tictactoe import Board
from tictactoe.tictactoe import AIPlayer
from tictactoe.tictactoe import Player
import simplejson

def home(request):
    """
        This view will return an html string to be rendered in the template representing the state of the game
        so that the view only ever renders one tic tac toe game at the time
    """
    # here we need to parse out the current state of the board so we can pass it to the class and render it

    if "board" in request.GET.keys():
        #were playing a game cause i got the board in the url
        win_message = None
        board = str(request.GET['board'])
        board = simplejson.loads(board)
        #create the board
        the_board = Board(the_board=board)
        #set the AI
        ai = AIPlayer('X')
        #set the human player
        human = Player('O')

        #look for the computer to win
        winning_position = ai.look_for_win(the_board)

        #if were gonna win make the move
        if winning_position:
            the_move = winning_position
        else:
            #otherwise have the AI take a move against the human
            the_move = ai.take_turn(the_board,human)

        #set the position on the board
        the_board.select_position(the_move,ai)

        #draw the board
        board_html = the_board.draw()

        if the_board.check_for_win(ai):
            win_message = "JaCK`s AnGry PAraKEet WINS"
        elif "" not in the_board.the_board:
            win_message = "JaCK`s AnGry PAraKEet WINS (cause JACK wins draws)"
    else:
        #draw the first step of the game, the computer always goes first
        board = ['','','','','X','','','','']
        the_board = Board(the_board=board)
        board_html = the_board.draw()

    return render_to_response('play/home.html',locals())