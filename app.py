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

    return jsonify(board=Board(board))

class Board:
    def __init__(self, board):
        # Tuples of every possible legit combo
        # Represented by XY pos, then square's value
        # Rows first top-bottom, then columns L-R, then diagonals
        self.orig_board = [
            [(0, 0, board[0][0]), (0, 1, board[0][1]), (0, 2, board[0][2])],
            [(1, 0, board[1][0]), (1, 1, board[1][1]), (1, 2, board[1][2])],
            [(2, 0, board[2][0]), (2, 1, board[2][1]), (2, 2, board[2][2])],
            [(0, 0, board[0][0]), (1, 0, board[1][0]), (2, 0, board[2][0])],
            [(1, 0, board[1][0]), (1, 1, board[1][1]), (1, 2, board[1][2])],
            [(0, 2, board[0][2]), (1, 2, board[1][2]), (2, 2, board[2][2])],
            [(0, 0, board[0][0]), (1, 1, board[1][1]), (2, 2, board[2][2])],
            [(0, 2, board[0][2]), (1, 1, board[1][1]), (0, 2, board[0][2])]
        ]
        self.ranked_triplets = []
        self.new_board = [[], [], []]
        self.player_letter = 'O'
        self.computer_letter = 'X'


    def prioritize_moves(self):
        for triplet in orig_board:
            player_can_win = tally_values(triplet)
            computer_can_win = talley_values(triplet, computer_letter)

        def tally_values(triplet, letter=player_letter):
            count = 0
            for square in triplet:
                if square[2] == letter:
                    count += 1
            if count == 2:
                return True
            else:
                return False

    return self.new_board

if __name__ == "__main__":
    app.run(debug=True)
