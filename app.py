from flask import Flask, jsonify, render_template, request
app = Flask( __name__ )

@app.route("/")
def setup_board():
    return render_template('board.html')

@app.route("/board", methods=['POST'])
def calculate_move():
    board = [
        request.form.getlist('board[top][]'),
        request.form.getlist('board[middle][]'),
        request.form.getlist('board[bottom][]')
    ]

    return jsonify(board=BoardWizard(board))

class BoardWizard:
    def __init__(self, board):
        self.orig_board = board
        self.new_board = []
        self.player_can_win = False
        self.computer_can_win = False

    def check_for_victory(self):
        pass

    def find_possible_moves(self):
        pass

    def check_next_move_winner(self):
        pass

    def prioritize_moves(self):
        pass

    return self.new_board

if __name__ == "__main__":
    app.run(debug=True)
