from django.views.generic import TemplateView

class GameView(TemplateView):
    template_name = 'tictactoe/gameview.html'

game_view = GameView.as_view()
