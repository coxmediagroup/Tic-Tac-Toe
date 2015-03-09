import json
from server import DynamicContentRequestHandler, run

HOST = ""   # listen on all interfaces
PORT = 9000

class RequestHandler(DynamicContentRequestHandler):
    def _evaluateBoard(self, board):
        return board, 'continue'

    def getMove(self, path, queryParms):
        board = list(queryParms['board'][0])
        newBoard, status = self._evaluateBoard(board)
        newBoard = ''.join(newBoard)
        content = json.dumps({'board': newBoard, 'status': status})
        return (content, 'application/json')

run(HOST, PORT, RequestHandler)
