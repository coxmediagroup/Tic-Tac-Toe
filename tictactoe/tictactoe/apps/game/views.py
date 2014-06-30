from django.http import Http404
from django.views.generic import TemplateView, View


class GameBoardView (TemplateView):
    """
    Displays the gameboard to the user.
    """
    template_name = 'apps/game/gameboard.html'


class SubmitMoveView (View):
    """
    Handles the AJAX game submissions submitted by the user.
    """
    def post(self, request, *args, **kwargs):
        # only accept ajax requests
        if not request.is_ajax():
            raise Http404