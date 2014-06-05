from app.ag.controller import BaseEndecaController
from core.http import JsonResponse
from core.http import TemplateResponse


class TicTacToeController(BaseEndecaController):
    """ Controller for the tic tac toe game.
    """

    def index(self, request, path, *args, **kwargs):

        # tic tac toe game env variables
        env = {}
        template = self.templates[path]

        return TemplateResponse(template, env)
