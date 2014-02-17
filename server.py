import board
import minimax
import movecache
import json
from bottle import route, run, static_file, request

@route('/api/omove', method='GET')
def omove():
    boardState = json.loads(request.query.get('board', None))
    gameBoard = board.Board(boardState)
    result = gameBoard.finished()
    move = None
    if not result[0]:
        moveCache = movecache.MoveCache()
        calc = minimax.MinimaxCalculator(moveCache) 
        move = calc.bestMove('O', gameBoard)
        gameBoard.move('O', move[0], move[1])
        result = gameBoard.finished()
    return {
                'result': {'gameOver':result[0], 'winner':result[1]},
                'move': move}

@route('/<filename>')
def staticFile(filename):
    return static_file(filename, './static')

@route('/')
def index():
    return static_file('index.html', './static')

run(host='localhost', port=8000)
