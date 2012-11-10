from flask import Flask, render_template, jsonify, request, json
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/computer/<round>')
def computer_turn(round=1):
    board = request.args.get("board[]", "")
    board = json.loads(board)
    # figure out what move to take based on current round and the board
    return jsonify(square=4)


if __name__ == '__main__':
    app.debug = True
    app.run()
