from flask import Flask, render_template, jsonify, request, json

from players import ComputerPlayerO

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/computer')
def computer_turn():
    round = request.args.get("round", 1, type=int)
    last_play = request.args.get("last_play", 0, type=int)
    board = request.args.get("board[]", "")
    board = json.loads(board)
    # figure out what move to take based on current round and the board
    computer = ComputerPlayerO(board, round)
    if round < 5:
        move = computer.play(last_play)
    else:
        move = 10  # bogus move, will stop game play
    game_over, winning_squares = computer.is_game_over()
    return jsonify(
        square=move,
        game_over=game_over,
        winning_squares=winning_squares
    )


if __name__ == '__main__':
    app.debug = True
    app.run()
