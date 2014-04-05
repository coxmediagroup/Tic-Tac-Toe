from ttt.models import TicTacToe
from django.contrib.auth.models import User
from datetime import datetime
import simplejson


def mark_square(request, game, player, row, col):
    ttt = TicTacToe.objects.get(id=game)
    ttt.update_board(player, (row, col))
    return HttpResponse(simplejson.dumps({'board':ttt.get_board()}), 
                        mimetype="application/json")

