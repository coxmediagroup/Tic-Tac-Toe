from flask import Flask, render_template, jsonify, request, json

from players import ComputerPlayerO

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/computer')
def computer_turn():
    board = request.args.get("board[]", "")
    board = json.loads(board)
    computer = ComputerPlayerO(board)
    move = computer.play()
    game_over, winning_squares = computer.is_game_over()
    return jsonify(
        square=move,
        game_over=game_over,
        winning_squares=winning_squares
    )


if __name__ == '__main__':
    app.debug = True
    app.run()
