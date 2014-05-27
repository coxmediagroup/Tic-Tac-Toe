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

    defensive_moves(board)
    offensive_moves(board)

    return jsonify(board=board)

def defensive_moves(board):
    def check_row(row):
        count = sum([1 for square in board[row] if square=='O'])
        if count == 2:
            for index, square in enumerate(board[row]):
                if square == '':
                    board[row][index] = 'X'

    def check_column(column):
        col = []
        for row in range(3):
            col.append(board[row][column])
        count = sum([1 for square in col if square=='O'])
        if count == 2:
            for row, square in enumerate(col):
                if square == '':
                    board[row][column] = 'X'

    def check_diagonals():
        diagonal1 = [board[0][0], board[1][1], board[2][2]]
        diagonal2 = [board[0][2], board[1][1], board[2][0]]
        count1 = sum([1 for square in diagonal1 if square=='O'])
        count2 = sum([1 for square in diagonal2 if square=='O'])
        if count1 == 2:
            if diagonal1[0] == '':
                board[0][0] = 'X'
            elif diagonal1[1] == '':
                board[1][1] = 'X'
            elif diagonal1[2] == '':
                board[2][2] = 'X'
        if count2 == 2:
            if diagonal2[0] == '':
                board[0][2] = 'X'
            elif diagonal2[1] == '':
                board[1][1] = 'X'
            elif diagonal2[2] == '':
                board[2][0] = 'X'

    for i in range(3):
        check_row(i)
        check_column(i)

    check_diagonals()


def offensive_moves(board):
    pass


if __name__ == "__main__":
    app.run(debug=True)
