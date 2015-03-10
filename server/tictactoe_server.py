import json
from server import DynamicContentRequestHandler, run
from tictactoe_ai import gameIsOver, findBestScoreMove

HOST = ""   # listen on all interfaces
PORT = 9000

class RequestHandler(DynamicContentRequestHandler):
    def _evaluateBoard(self, board):
        """
        1. determines if game is over, and if so, who won (or whether it's a draw).
        2. if game is not over, determines/makes next move and returns
            - the new board
            - the status:
                'continue': game not over
                'iwin': AI won
                'uwin': player won
                'draw': game is over, but neither player won
            - the status positions:
                if status is 'continue' or 'draw', status positions is []
                if status is 'iwin' or 'uwin', status positions is a list
                    containing the indexes of the three-in-a-row

        """

        status = gameIsOver(board)

        if status:
            winner, positions = status
            if winner is 'O':
                return board, 'iwin', positions
            elif winner is 'X':
                return board, 'uwin', positions
            else:
                return board, 'draw', []
        else:
            # game not over so select a move
            _score, pos = findBestScoreMove(board)
            board[pos] = 'O'

            # see if game over now
            status = gameIsOver(board)

            if status:
                winner, positions = status
                if winner is 'O':
                    return board, 'iwin', positions
                else:
                    return board, 'draw', []
            else:
                return board, 'continue', []

    def evalBoard(self, path, queryParms):
        board = list(queryParms['board'][0])
        newBoard, status, positions = self._evaluateBoard(board)
        newBoard = ''.join(newBoard)
        content = json.dumps(
            {'board': newBoard,
             'status': status,
             'positions': positions})
        return (content, 'application/json')

run(HOST, PORT, RequestHandler)
