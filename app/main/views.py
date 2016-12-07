import json
from django.http import StreamingHttpResponse
from django.views.generic import TemplateView
from minimax.minimax import play_turn

class BoardView(TemplateView):
    template_name = 'board.html'

def make_a_move(request):
    # Decode the json into python
    board = json.loads(request.GET['board'])
    # Make a move
    status, board = play_turn(board=board)
    data = {'status': status, 'board': board}
    return StreamingHttpResponse(json.dumps(data), content_type='application/json')
