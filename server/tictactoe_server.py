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

        # game over if there's 3 in a row
        if self._threeInARow('O', board):
            print("iwin. board =", board)
            return board, 'iwin'
        elif self._threeInARow('X', board):
            print("uwin. board =", board)
            return board, 'uwin'

        # game also over if no empty squares, it's a draw
        if '-' not in board:
            return board, 'draw'

        # game not over so select a move
        board = self._makeMove(board)

        # see if game over now
        if self._threeInARow('O', board):
            return board, 'iwin'
        if '-' not in board:
            return board, 'draw'

        return board, 'continue'

    def _threeInARow(self, char, board):
        """
            board is a list of 9 elements, representing 3 rows of 3 columns:
                0   1   2
                3   4   5
                6   7   8
        """
        print("_threeInARow. char = %s, board = %s"%(char, board))
        def _charAtAllPositions(board, char, positions):
            for position in positions:
                if board[position] != char:
                    return False
            return True

        positionsList = [
            (0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
                (0,4,8), (2,4,6)           ]

        for positions in positionsList:
            if _charAtAllPositions(board, char, positions):
                return True
        return False

    def _makeMove(self, board):
        # replace first '-' with 'O'
        i = board.index('-')
        board[i] = 'O'
        return board

    def evalBoard(self, path, queryParms):
        board = list(queryParms['board'][0])
        newBoard, status = self._evaluateBoard(board)
        newBoard = ''.join(newBoard)
        content = json.dumps({'board': newBoard, 'status': status})
        return (content, 'application/json')

run(HOST, PORT, RequestHandler)
