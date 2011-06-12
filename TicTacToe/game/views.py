
import json
from django import shortcuts
from django import http
import game

def index(request):
    if request.method == "GET":
        return shortcuts.render_to_response('index.html')
    else:
        board = json.loads(request.POST['board'])
        ttt = game.TicTacToe('O')
        updated_board = ttt.make_move(board)
        response = json.dumps(dict(board=updated_board, winner=ttt.winner(updated_board)))
        return http.HttpResponse(response, mimetype='application/json')
