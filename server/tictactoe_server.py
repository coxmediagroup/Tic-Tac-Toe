import json
from server import DynamicContentRequestHandler, run

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

        # game over if there's 3 in a row
        positions = self._threeInARow('O', board)
        if positions: return board, 'iwin', positions

        positions = self._threeInARow('X', board)
        if positions: return board, 'uwin', positions

        # game also over if no empty squares, it's a draw
        if '-' not in board: return board, 'draw', []

        # game not over so select a move
        board = self._makeMove(board)

        # see if game over now
        positions = self._threeInARow('O', board)
        if positions: return board, 'iwin', positions
        if '-' not in board: return board, 'draw', []

        return board, 'continue', []

    def _threeInARow(self, char, board):
        """
            board is a list of 9 elements, representing 3 rows of 3 columns:
                0   1   2
                3   4   5
                6   7   8
        """
        def _charAtAllPositions(board, char, positions):
            for position in positions:
                if board[position] != char:
                    return False
            return True

        winningPositionsList = [
            (0,1,2), (3,4,5), (6,7,8),  # 3 across
            (0,3,6), (1,4,7), (2,5,8),  # 3 down
                (0,4,8), (2,4,6)        # 3 diagonal
        ]

        for positions in winningPositionsList:
            if _charAtAllPositions(board, char, positions):
                return positions
        return False

    def _makeMove(self, board):
        # replace first '-' with 'O'
        i = board.index('-')
        board[i] = 'O'
        return board

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
