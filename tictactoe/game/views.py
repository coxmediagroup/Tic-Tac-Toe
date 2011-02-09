from django.shortcuts import redirect, get_object_or_404, render_to_response
from game.models import Game
from game.ai import perform_move

def new_game(request):
    "Create a new game and redirect to its url."
    game = Game()
    perform_move(game)  # Computer goes first
    game.save()
    return redirect(game)

def show_game(request, game_id):
    "Show a specific game."
    game = get_object_or_404(Game, pk=game_id)
    return render_to_response("game/show_game.html", { 'game': game })

def make_move(request, game_id):
    """
    Make a move.

    This method should be called asynchronously and will return the new game
    board state rendered as HTML.
    """
    game = get_object_or_404(Game, pk=game_id)

    if 'row' not in request.POST or 'column' not in request.POST:
        # Can't do anything if we don't know which cell was clicked.
        return render_to_response("game/_board.html", { 'game': game })

    row, column = int(request.POST['row']), int(request.POST['column'])
    if game.board_state[row][column] is None:
        game.board_state[row][column] = 'O'
        if not game.is_game_over():
            perform_move(game)
        game.save();

    return render_to_response("game/_board.html", { 'game': game })
