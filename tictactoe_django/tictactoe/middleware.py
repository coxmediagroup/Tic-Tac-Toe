from models import *

class GameSetupMiddleware:
    def process_request(self, request):
        if 'gamestate' not in request.session or not request.session['gamestate']:
            request.session['gamestate'] = GameState()
