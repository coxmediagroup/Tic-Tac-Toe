import json
from django.http import StreamingHttpResponse
from django.views.generic import TemplateView

class BoardView(TemplateView):
    template_name = 'board.html'

def home_view(request):
    content = 'Hello World!'
    return HttpResponse(content)

def make_a_move(request):
    # Decode the json into python
    board = json.loads(request.GET['board'])
    # Make a move
    if 0 in board:
        board[board.index(0)] = 2
    return StreamingHttpResponse(json.dumps(board), content_type='application/json')
