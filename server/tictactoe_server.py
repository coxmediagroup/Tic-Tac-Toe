import json
from server import DynamicContentRequestHandler, run
from tictactoe_ai import gameIsOver, findBestScoreMove
from random import choice

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

        # if board is empty, just randomly select a corner and be done with it.
        if board.count('-') == 9:
            # corners are 0, 2, 6, and 8
            pos = choice([0,2,6,8])
            board[pos] = 'O'
            return board, 'continue', []

        # board isn't empty, so examine board to see if we have a draw or a winner
        status = gameIsOver(board)
        if status:
            # yep, game's over, so return the results.
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
        """ Since this is a public method, its name will become a public
            web service.  Any calls to this web service will be handled
            by this method.

            This method examines the 'board' query parameter and returns
            a JSON object containing 3 attributes:
                * board - the received board plus any move the AI made.
                * status - one of 'uwin', 'iwin', 'draw', 'continue'
                * positions - a list of 3 positions if status is 'iwin' or 'uwin'
        """
        board = list(queryParms['board'][0])
        newBoard, status, positions = self._evaluateBoard(board)
        newBoard = ''.join(newBoard)
        content = json.dumps(
            {'board': newBoard,
             'status': status,
             'positions': positions})
        return (content, 'application/json')

run(RequestHandler)
