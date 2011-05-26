from Game.board import create_computer_move, empty, empty_board, isGameOver, Player_O, Player_X

from django.shortcuts import HttpResponseRedirect, render_to_response

def begin_game(request,  template_name='board.html'):
    '''
       the main view function, 
       if first time loading, give the user the empty_board
       else, checks to see if the game is over
       also will reset the messages used in the template
    '''
    if "game_board" not in request.session:
        request.session['game_board'] = empty_board

    board = request.session["game_board"]
    user_message = "Make your move"
    game_over = False

    #checks for empty spaces in board, if none, the game is a tie
    if empty not in board:
        user_message = "The game is a Tie"
        game_over = True
    #calls the isGameOver function, which checks for no empty spaces, also if 
    #a winning layout has been acomplished
    if isGameOver(board):
        user_message = "The game is over"
        game_over = True

    context = { 'board': board,
                'empty': empty,
                'user_message': user_message,
                'game_over': game_over }

    return render_to_response(template_name, context)


def game_move(request):
    '''
         Get the player move from the request & update the game_board,
         then calculate the next best move and play it.
    '''
    board = request.session["game_board"]
    move = request.GET.get('button')
    player_move = int(move)
    board[player_move] = Player_X # X is a player move

    #if a space is anywhere in the board, its the computers turn
    if empty in board:
        computer_move = create_computer_move(board)
        board[computer_move] = Player_O

    request.session["game_board"] = board
    return HttpResponseRedirect('/')


def reset_game(request):
    '''
        this resets the game to the empty_board layout
    '''
    request.session["game_board"] = empty_board
    board = request.session["game_board"]
    user_message = "Welcome to a new game of TicTacToe!"
    game_over = False
    context = { 'board': board,
                'empty': empty,
                'user_message': user_message,
                'game_over': game_over }
    return render_to_response('board.html', context)
