from django.views.generic import TemplateView

from tictactoe.game.game import Gameboard

def _fetch_gameboard(request):
    gameboard = request.session.get('gameboard', None)
    if not gameboard:
        gameboard = Gameboard()
        request.session['gameboard'] = gameboard
    return gameboard

class GameView(TemplateView):
    template_name = "game.html"
    
    def get(self, request, **kwargs):
        return self.render_to_response(self.get_context_data(request, **kwargs))
    
    def post(self, request, **kwargs):
        reset = request.POST.get('reset')
        move = request.POST.get('submit')
        if reset:
            request.session['gameboard'] = None
        if move:
            return self.render_to_response(self.do_move(request, **kwargs))
        return self.render_to_response(self.get_context_data(request, **kwargs))
    
    def do_move(self, request, **kwargs):
        # do game logic
        gameboard = _fetch_gameboard(request)
        gameboard.change()
        request.session['gameboard'] = gameboard
        context = self.get_context_data(request, **kwargs)
        context['message'] = 'Invalid move!'
        context['post'] = request.POST
        return context
    
    def get_context_data(self, request, **kwargs):
        context = super(GameView, self).get_context_data(**kwargs)
        context['gameboard'] = _fetch_gameboard(request)
        return context
