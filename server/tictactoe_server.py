import json
from server import DynamicContentRequestHandler, run

HOST = ""   # listen on all interfaces
PORT = 9000

class RequestHandler(DynamicContentRequestHandler):
    def _evaluateBoard(self, board):
        """
        1. determines if game is over, and if so, who won (or whether it's a draw).
        2. if game is not over, determines/makes next move and returns
            - the new board, and
            - the status:
                'continue': game not over
                'iwin': AI won
                'uwin': player won
                'draw': game is over, but neither player won
        """
        # replace first '-' with 'O'
        i = board.index('-')
        board[i] = 'O'
        return board, 'continue'

    def evalBoard(self, path, queryParms):
        board = list(queryParms['board'][0])
        newBoard, status = self._evaluateBoard(board)
        newBoard = ''.join(newBoard)
        content = json.dumps({'board': newBoard, 'status': status})
        return (content, 'application/json')

run(HOST, PORT, RequestHandler)
