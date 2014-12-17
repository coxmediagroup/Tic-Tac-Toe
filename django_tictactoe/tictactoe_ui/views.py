from django.shortcuts import render, redirect

from tictactoe_api.models.persistent_game_state import PersistentGameState

def index(request):
  "return all the games for which there's been a recorded move"
  gameIds = list(PersistentGameState.getAllGameIds())
  return render(request, "index.html", {'gameIds':gameIds})

def html_form_response(request, game, msg=None):
  "Capture the request object for rendering the response"
  squares = list(enumerate(game.board))
  rows = [squares[0:3], squares[3:6], squares[6:9]]
  return render(request, "game.html", {"game": game, "rows": rows, "msg": msg})

def new_game(request):
  "synthesize a new ID and redirect to it. The returned Game ID is ephemeral until a move is posted"
  if request.method != 'POST':
    return render(request, "error.html", {"message":"Must POST to get a new game ID"})
  else:
    game_id = PersistentGameState.generate_id()
    return redirect('game', game_id=game_id)

def game(request, game_id):
  game = PersistentGameState.load(game_id)
  if request.method != 'POST':
    return html_form_response(request, game)
  else:
    player = request.POST['player']
    position = int(request.POST['position'])
    return game.execute_move(
      player,
      position,
      onValid = lambda game: computer_move_response(request, game),
      onInvalid = lambda reason: html_form_response(request, game, "You attempted an invalid move: " + reason)
    )

def computer_move_response(request, game):
  "Act as the computer opponent. if the game is finished, just return it. "
  "Otherwise find a move with the minmax algorithm and play it"
  if game.isFinished():
    return html_form_response(request, game, "Game is over.")
  else:
    computer_player = game.next_player()
    _, computer_move = game.suggest_next(computer_player)
    return game.execute_move(
      computer_player,
      computer_move,
      onValid = lambda game: html_form_response(request, game, "Computer has moved."),
      onInvalid = lambda reason: html_form_response(request, game, "Computer made an invalid move: " + reason)
      )
