from rest_framework.views import APIView
from rest_framework.response import Response

from tictactoe.api.ai import TicTacToeNode, get_recommended_play

# warm up the cache
get_recommended_play(TicTacToeNode())


class RecommendedPlay(APIView):
    """ Given a list of tic-tac-toe moves,
    return the recommended next move.
    """
    def post(self, request, format=None):
        moves = request.DATA.get("moves", [])
        try:
            node = TicTacToeNode.from_history(*moves)
        except ValueError as e:
            return Response({
                "error": str(e),
            }, status=404)
        if node.terminal:
            next_move = None
        else:
            recommended_play = get_recommended_play(node)
            next_move = recommended_play.move
            moves += [recommended_play.move]

        return Response({
            "moves": moves,
            "next_move": next_move,
        })
