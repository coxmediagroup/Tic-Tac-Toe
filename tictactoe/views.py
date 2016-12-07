from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.shortcuts import render

from tictactoe.ai import get_best_move
from tictactoe.forms import SelectionForm
from tictactoe.models import Board

def show_board(request):
    """
    Renders the Game Board
    """
    # Ensure a Game is in Progress
    board_id = request.session.get('board_id', None)
    if board_id:
        try:
            board = Board.objects.get(id=board_id)
            print "Board ID: %s" % board_id
        except ObjectDoesNotExist:
            messages.warning(request, "The game you were playing is gone.")
            return redirect('new-game')
    else:
        return redirect('new-game')

    # Check for Victory
    if board.victory_status() == -1:
        messages.warning(request, 'The Computer has won the Game')
    elif board.victory_status() == 1:
        messages.success(request, 'You have miraculously won the Game!')
    elif board.victory_status() == 0:
        messages.info(request, 'The Game has ended in a Draw')

    return render(request, 'app.html', { 'board': board })


def select_piece(request):
    """
    Accepts a Piece Selection from a User, executes the Computer Player's next
    move, and redirects the User back to the `game_view`.
    """
    # Ensure a Game is in Progress
    board_id = request.session.get('board_id', None)
    if board_id:
        try:
            board = Board.objects.get(id=board_id)
        except ObjectDoesNotExist:
            messages.warning(request, "The game you were playing is gone.")
            return redirect('new-game')
    else:
        return redirect('new-game')

    # Insert the Player's and Computer's Selections
    if request.method == 'POST' and board.victory_status() == None:
        form = SelectionForm(request.POST)
        if form.is_valid():
            selection = form.cleaned_data['selection']
            if getattr(board, selection) == 0:
                setattr(board, selection, 1)
                if board.victory_status() == None:
                    computer_selection = get_best_move(board, -1)
                    if computer_selection:
                        setattr(board, computer_selection, -1)
                board.save()
            else:
                messages.warning(request, "Cannot place a Game Piece here")

    return redirect('home')


def end_game(request):
    """ 
    Ends the current game and redirects the User to play a new Game.
    """
    # Delete the current Game from both the Browser Session and Database.
    board_id = request.session.get('board_id', None)
    if board_id:
        request.session.pop('board_id')
        try:
            board = Board.objects.get(id=board_id)
            board.delete()
        except ObjectDoesNotExist:
            return redirect('new-game')

    # Redirect to create a New Game
    return redirect('new-game')


def new_game(request):
    """
    Starts a New Game
    """
    board = Board.objects.create()
    request.session['board_id'] = board.id
    messages.success(request, "New Game Started. It's your turn. Good luck!")
    return redirect('home')
