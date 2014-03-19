from django.shortcuts import render

import play.utilities as util
from play.models import Game

# Create your views here.
def index(request):
    return render(request, "index.html")

def move(request):
    import json
    #import movelogic
    
    # Make sure we have an active game
    if 'board_id' not in request.session:
        # new game
        try:
            game = Game()
            game.save()
            request.session['board_id'] = game.id
        except:
            return util.json_response(False, "Error accessing database.")
    
    # At this point we have an active game -- use it!
    util.json_response(True, "Move made")
