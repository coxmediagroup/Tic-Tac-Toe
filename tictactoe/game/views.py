from django.views.generic import TemplateView

from tictactoe.game.game import Gameboard

def _fetch_gameboard(request):
    """
    Check session for saved gameboard or instantiate new gameboard
    """
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
        """
        Check for valid POST data, then attempt player's move
        """
        reset = request.POST.get('reset')
        position = request.POST.get('position')
        move = request.POST.get('move')
        if reset:
            request.session['gameboard'] = None
        if position and move:
            position = list(position)
            for index, item in enumerate(position):
                position[index] = int(item)
            return self.render_to_response(self.do_move(request, position, **kwargs))
        return self.render_to_response(self.get_context_data(request, **kwargs))
    
    def do_move(self, request, position, **kwargs):
        """
        Check for valid move, then run AI routine if no winner
        """
        gameboard = _fetch_gameboard(request)
        if position not in gameboard.available_spaces():
            context = self.get_context_data(request, **kwargs)
            context['message'] = 'Invalid move!'
            return context
        gameboard.save_move(position, 1)
        finished = gameboard.check_status(1)
        if not finished:
            gameboard.calc_computer_move()
            finished = gameboard.check_status(-1)
        request.session['gameboard'] = gameboard
        context = self.get_context_data(request, **kwargs)
        if finished:
            context['message'] = gameboard.status
        return context
    
    def get_context_data(self, request, **kwargs):
        """
        Add gameboard to view context
        """
        context = super(GameView, self).get_context_data(**kwargs)
        context['gameboard'] = _fetch_gameboard(request)
        return context
