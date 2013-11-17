from itertools import repeat
import json
from django.http.response import HttpResponseBadRequest
from django.views.generic.base import TemplateView
from third_party.tictactoe import whoGoesFirst, getComputerMove, makeMove, isWinner, isBoardFull


class GameView(TemplateView):
    template_name = "game.html"

    def get(self, request, *args, **kwargs):
        self.board = list(repeat('', 10))
        self.start_game()
        return super(GameView, self).get(request, *args, **kwargs)

    def start_game(self):
        board = self.board
        start = whoGoesFirst()
        #start = "computer"
        print start
        if start == "computer":
            computer_letter = "X"
            move = getComputerMove(board, computer_letter)
            makeMove(board, computer_letter, move)

    def get_context_data(self, **kwargs):
        context = super(GameView, self).get_context_data(**kwargs)
        context["board"] = self.board[1:]
        context["board_json"] = json.dumps(self.board[1:])
        context["message"] = "Please click on an empty square."
        return context

    def __init__(self, **kwargs):
        super(GameView, self).__init__(**kwargs)
        self.board = []


class PlayerMove(TemplateView):
    template_name = "board_snippet.html"
    http_method_names = ["post"]

    def evaluate_board(self, letter):
        """
        Return values:
            0 Nothing
            1 Win
            2 Draw
        """
        board = self.board
        result = isWinner(board, letter)
        if not result and isBoardFull(board):
            result = 2
        return result

    def computer_move(self, board):
        pass

    def get_context_data(self, **kwargs):
        context = super(PlayerMove, self).get_context_data(**kwargs)
        context["board"] = self.board
        context["board_json"] = json.dumps(self.board)
        context["message"] = self.message

        return context

    def post(self, request):
        board_json = request.POST.get("board", "[]")
        board = json.loads(board_json)
        if not isinstance(board, list) or not len(board) == 9:
            return HttpResponseBadRequest("You gave me a bad board or none at all.")

        # get the respective players' letter
        num_moves = len(filter(None, board))
        if num_moves % 2:
            player_letter = "X"
            computer_letter = "O"
        else:
            player_letter = "O"
            computer_letter = "X"

        # put an empty value at the start so the board is compatible with the external lib
        board.insert(0, "")

        board_result = self.evaluate_board(player_letter)
        winner = None
        if not board_result:
            move = getComputerMove(board, computer_letter)
            makeMove(board, computer_letter, move)
            board_result = self.evaluate_board(computer_letter)
            if board_result == 1:
                winner = "Computer"
        else:
            winner = "Player"

        if board_result or winner:
            if winner:
                self.message = "%s won!" % winner
            elif board_result == 2:
                self.message = "Draw!"
            else:
                return HttpResponseBadRequest("How did the board evaluate to that?")

        self.board = board[1:]
        context = self.get_context_data()
        return self.render_to_response(context)

    def __init__(self, **kwargs):
        super(PlayerMove, self).__init__(**kwargs)
        self.board = []
        self.message = "Please click on an empty square."
