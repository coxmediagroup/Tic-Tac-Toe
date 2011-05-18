# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from tictac.mainapp.game_rules import calc_computer_move, calc_game_over

def paint_board(request):
    ''' Paint the game state into the board gui (board.html) 
        X = Human player
        O = Computer player
        _ = empty space
        The game ends with a tie when there are no empty spaces left to play 
        or when somebody wins (calc_game_over = True ). 
    '''
    if "game_board" not in request.session:
        request.session["game_board"] = ["_","_","_","_","_","_","_","_","_"]
    board = request.session["game_board"]

    b0 = board[0]
    b1 = board[1]
    b2 = board[2]
    b3 = board[3]
    b4 = board[4]
    b5 = board[5]
    b6 = board[6]
    b7 = board[7]
    b8 = board[8]
    user_message = "Make your move"
    game_over = False
    
    if "_" not in board:                     
       user_message = "it is a tie !!! "
       game_over = True
    
    if calc_game_over(board):
       user_message = "game over !!! "
       game_over = True
       
    return render_to_response('board.html', locals())
    
def process_move(request):
    ''' Get the player move from the request & update the game_board,
        then calculate the next best move and play it.
    '''
    board = request.session["game_board"]
    move = request.GET.get('button')
    m = int(move)  
    board[m] = "X" # X is a player move 
    
    if "_" in board: # if last space is played, skip computers turn
      c = calc_computer_move(board) 
      board[c] = "0" 
      
    request.session["game_board"] = board
    return HttpResponseRedirect('/board') 
       
def reset(request):
    ''' Clear the game board state to start a new game. 
    '''
    request.session["game_board"] = ["_","_","_","_","_","_","_","_","_"]
    board = request.session["game_board"]
    b0 = b1 = b2 = b3 = b4 = b5 = b6 = b7 = b8 = "_"
    user_message = "Welcome to a new Game!! "
    game_over = False
 
    return render_to_response('board.html', locals())
