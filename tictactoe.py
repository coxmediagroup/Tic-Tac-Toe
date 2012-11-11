import random

from flask import Flask, render_template, jsonify, request, json
app = Flask(__name__)

CORNERS = [0, 2, 6, 8]
WALLS = [1, 3, 5, 7]
CENTER = 4
WINNING_MOVES = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]


class TicTacToePlayer(object):
    def __init__(self, board):
        self.board = board

    rounds = [
        'round_one',
        'round_two',
        'round_three',
    ]

    def round_one(self, last_play):
        if last_play in CORNERS:
            return CENTER
        return random.choice(CORNERS)

    def round_two(self, last_play):
        needs_blocked, play = self.block_win()
        if needs_blocked:
            return play
        if last_play in CORNERS:
            # tie game
            return random.choice([1, 7])
        return random.choice(self.remaining_corners)

    def round_three(self, last_play):
        needs_blocked, play = self.block_win()
        if needs_blocked:
            return play
        can_win, play = self.winning_move()
        if can_win:
            return play
        if CENTER not in self.xes_and_oes:
            return CENTER
        return random.choice(self.remaining_spaces)

    def play(self, round, last_play):
        # find the function to call for the specified round in self.rounds
        # and call it to get the next move
        round_method = getattr(self, self.rounds[round - 1])
        return round_method(last_play)

    @property
    def xes(self):
        return [x for x, square in enumerate(self.board) if square['has_x']]

    @property
    def oes(self):
        return [o for o, square in enumerate(self.board) if square['has_o']]

    @property
    def xes_and_oes(self):
        return self.xes + self.oes

    @property
    def remaining_corners(self):
        return [i for i in CORNERS if i not in self.xes_and_oes]

    @property
    def remaining_walls(self):
        return [i for i in WALLS if i not in self.xes_and_oes]

    @property
    def remaining_spaces(self):
        spaces = CORNERS + WALLS + CENTER
        return [space for space in spaces if space not in self.xes_and_oes]

    def block_win(self):
        for win in WINNING_MOVES:
            xes_in_win = [x for x in self.xes if x in win]
            if len(xes_in_win) == 2:
                oes_in_win = [o for o in self.oes if o in win]
                if not oes_in_win:
                    return True, [x for x in win if x not in xes_in_win][0]
        return False, False

    def can_win(self):
        for win in WINNING_MOVES:
            oes_in_win = [o for o in self.oes if o in win]
            if len(oes_in_win) == 2:
                xes_in_win = [x for x in self.xes if x in win]
                if not xes_in_win:
                    return True, [o for o in win if o not in oes_in_win]
        return False, False


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/computer')
def computer_turn():
    round = request.args.get("round", 1, type=int)
    last_play = request.args.get("last_play", 0, type=int)
    board = request.args.get("board[]", "")
    board = json.loads(board)
    # figure out what move to take based on current round and the board
    computer = TicTacToePlayer(board)
    move = computer.play(round, last_play)
    return jsonify(square=move)


if __name__ == '__main__':
    app.debug = True
    app.run()
