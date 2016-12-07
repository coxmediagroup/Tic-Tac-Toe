import json

from app.ag.controller import BaseEndecaController
from app.ag.model.tictactoegame import TicTacToeGame
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

    def evaluate_board(self, request):
        """ Evaluate a tic tac toe board.
        """
        board = request.params.get('board')

        # create a game and evaluate the board
        game = TicTacToeGame()
        turn_result = game.take_a_turn(json.loads(board))

        # return turn data to client
        return JsonResponse(turn_result)

