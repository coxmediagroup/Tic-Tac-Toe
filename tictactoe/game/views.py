from django.views.generic import TemplateView

class GameView(TemplateView):
    template_name = "game.html"
    
    def do_move(self, request, **kwargs):
        # do game logic
        context = super(GameView, self).get_context_data(**kwargs)
        context['message'] = 'Invalid move!'
        return context
    
    def post(self, request, **kwargs):
        return self.render_to_response(self.do_move(request, **kwargs))
