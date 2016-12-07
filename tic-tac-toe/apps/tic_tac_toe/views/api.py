from rest_framework import views, exceptions, status
from rest_framework.response import Response

from lib.tic_tac_toe import TicTacToeGame, ComputerPlayer, GAME_STATUS


class GamePlayView(views.APIView):
    """Handles the interaction with the human player"""
        
    def post(self, request):
        data = request.DATA
        # 'ok computer', do your magic
        game = self._build_game(data['board'])
        
        if game is None:
            raise BadRequestError('Game could not be created with board %r' %
                                  (data['board'],))
        ComputerPlayer().do_move(game)
        
        # build response data
        game_status = game.status
        board_data = dict(board=game.board, status=game_status)
        
        if game_status == GAME_STATUS.WIN:
            board_data['winner'] = game.winner

        # send it back.
        return Response({'success': True, 'data': board_data})
    
    def _build_game(self, board):
        try:
            return TicTacToeGame.from_game(board)
        except Exception:
            pass # Explicitly silenced: check out "import this" 8^)
        return None


class BadRequestError(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Malformed request.'