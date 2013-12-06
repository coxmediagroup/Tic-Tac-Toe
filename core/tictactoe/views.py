from core.utils import CBVBaseView
from django.views.decorators.csrf import csrf_exempt


def get_possible_moves(board, token):
    human = 'X' if token == 'O' else 'O'
    moves = {
        "p1": None,
        "p2": None,
        "p3": None,
        "p4": None,
        "p5": None,
        "p6": None,
        "p7": None
    }
    movelist = []
    for move, spot in board.iteritems():
        if spot != 'X' and spot != 'O' and len(move) < 3:
            movelist.append(move)

    # p1: win if possible, can't lose if the game is over
    for move in movelist:
        board[move] = token
        if victory(board, move):
            moves['p1'] = move
            return moves
        board[move] = ''

    # p2: keep opponent from winning
    for move in movelist:
        board[move] = human
        if victory(board, move):
            moves['p1'] = move
            return moves
        board[move] = ''

    # p3: create multiple opportunities for yourself

    # p4: block opponent from setting up multiple win scenarios

    # p5: take the center if its available
    if 'm5' in movelist:
        moves['p5'] = 'm5'
        return moves

    # p6: get a corner opposite of your opponent if possible
    if 'm1' in movelist and 'm9' not in movelist:
        pass
    if 'm3' in movelist and 'm7' not in movelist:
        pass
    if 'm7' in movelist and 'm3' not in movelist:
        pass
    if 'm9' in movelist and 'm3' not in movelist:
        pass

    # p7: just take any corner while you're at it. you might as well
    if 'm1' in movelist:
        moves['p7'] = 'm1'
        return moves
    if 'm3' in movelist:
        moves['p7'] = 'm3'
        return moves
    if 'm7' in movelist:
        moves['p7'] = 'm7'
        return moves
    if 'm9' in movelist:
        moves['p7'] = 'm9'
        return moves

    # p8: only possible move left to make is taking the middle on
    # on an edge side. But that will be taken care of elsewhere.

    return moves


def make_move(board, token, move = None):
    # base case is to take the middle of an edge
    b = board
    if move == None:
        if board["m2"] == "":
            b["m2"] = token
            b['latest'] = 'm2'
            return b
        elif board["m4"] == "":
            b["m4"] = token
            b['latest'] = 'm4'
            return b
        elif board["m6"] == "":
            b["m6"] = token
            b['latest'] = 'm6'
            return b
        elif board["m8"] == "":
            b["m8"] = token
            b['latest'] = 'm8'
            return b
        else:
            return board
    # otherwise make the highest priority move
    # found in get_possible_moves
    else:
        b[move] = token
        b['latest'] = move
        return b


def victory(board, last):
    checks = {
        "m1": [('m2', 'm3'), ('m5', 'm9'), ('m4', 'm7')],
        "m2": [('m1', 'm3'), ('m5', 'm8')],
        "m3": [('m1', 'm2'), ('m5', 'm7'), ('m6', 'm9')],
        "m4": [('m1', 'm7'), ('m5', 'm6')],
        "m5": [('m1', 'm9'), ('m3', 'm7'), ('m2', 'm8'), ('m4', 'm6')],
        "m6": [('m3', 'm9'), ('m4', 'm5')],
        "m7": [('m1', 'm4'), ('m5', 'm3'), ('m8', 'm9')],
        "m8": [('m7', 'm9'), ('m5', 'm2')],
        "m9": [('m7', 'm8'), ('m1', 'm5'), ('m3', 'm6')],
    }

    token = board[last]

    for pair in checks[last]:
        a = (board[pair[0]] == token)
        b = (board[pair[-1]] == token)
        if a and b:
            return True

    return False


def draw(board):
    for key, value in board.iteritems():
        if value != 'X' and value != 'O' and len(key) < 3:
            return False
    return True



class TicTacToeView(CBVBaseView):
    def get(self, request):
        token = "error"
        order = request.GET.get('order')
        if order == 'first':
            token = "X"
        elif order == 'second':
            token = "O"
        else:
            raise ValueError(order)
        return self.to_template(data={"token":token})


    def post(self, request):
        token = request.POST['token']
        pctoken = 'X' if token == 'O' else 'O'
        board = {
            'm1': request.POST["m1"], 'm2': request.POST["m2"], 'm3': request.POST["m3"],
            'm4': request.POST["m4"], 'm5': request.POST["m5"], 'm6': request.POST["m6"],
            'm7': request.POST["m7"], 'm8': request.POST["m8"], 'm9': request.POST["m9"],
            'status': '', 'latest': '', 'gamestate': request.POST["gamestate"]
        }
        if board['gamestate'] in ['victory', 'draw']:
            board['status'] = "The game is already over!"
            return self.to_json(board)

        move = request.POST["move"]
        if move in board and board[move] != "":
            board["status"] = "That is an invalid move"
            return self.to_json(board)
        else:
            board[move] = token

        if victory(board, move):
            board["status"] = "ERROR: You have won! That was not supposed to happen!"
            board["gamestate"] = "victory"
            return self.to_json(board)
        if draw(board):
            board["status"] = "The game has ended in a draw!"
            board["gamestate"] = "draw"
            return self.to_json(board)
        
        moves = get_possible_moves(board, pctoken)
        if moves['p1']:
            board = make_move(board, pctoken, moves['p1'])
        elif moves['p2']:
            board = make_move(board, pctoken, moves['p2'])
        elif moves['p3']:
            board = make_move(board, pctoken, moves['p3'])
        elif moves['p4']:
            board = make_move(board, pctoken, moves['p4'])
        elif moves['p5']:
            board = make_move(board, pctoken, moves['p5'])
        elif moves['p6']:
            board = make_move(board, pctoken, moves['p6'])
        elif moves['p7']:
            board = make_move(board, pctoken, moves['p7'])
        else:
            board = make_move(board, pctoken)

        if victory(board, board['latest']):
            board["status"] = "The computer has won. Long live AI!"
            board["gamestate"] = "victory"
        elif draw(board):
            board["status"] = "The game has ended in a draw!"
            board["gamestate"] = "draw"

        return self.to_json(board)


