
class GameSetupMiddleware:
    def process_request(self, request):
        if 'gamestate' not in request.session or not request.session['gamestate']:
            print "Resetting game state"
            reset_gamestate(request)
            request.session.modified = True

from models import *
from functions import reset_gamestate