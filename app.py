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
        self.orig_board = board
        self.possible_moves = []
        self.new_board = [[],[],[]]
        self.player_can_win = False
        self.computer_can_win = False
        self.player_letter = 'O'
        self.computer_letter = 'X'

    def check_for_victory(self):
        pass

    def find_possible_moves(self):
        cols = []
        for rowindex, row in enumerate(self.orig_board):
            self.predict_winner_rows(rowindex)
            for colindex, square in enumerate(row):
                self.predict_winner_cols(cols, colindex)
                cols.append(self.orig_board[rowindex][colindex])
                if self.orig_board[rowindex][colindex] == '':
                    self.possible_moves.append([row,col])

    def predict_winner_rows(self, rowindex, letter=player_letter):
        check_row = sum([1 for square in self.orig_board[rowindex] if square == letter])
        if check_row == 2:
            for index, square in enumerate(self.orig_board[rowindex]:
                    if square == '':
                        self.possible_moves[rowindex][index] == 'X1'

    def predict_winner_cols(self, cols, colindex, letter=player_letter):
        check_col = sum([1 for square in cols if square == letter])
        if check_col == 2:
            for row, square in enumerate(cols):
                if square == '':
                    self.possible_moves[row][colindex]

    def prioritize_moves(self):
        pass

    return self.new_board

if __name__ == "__main__":
    app.run(debug=True)
