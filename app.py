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

    def check_diagonals(diagonal):
        count = sum([1 for square in diagonal if square=='O'])
        if count == 2:
            if diagonal[0] == '':
                board[diagonal["positions"][0]][diagonal["positions"][1]] = 'X'
            elif diagonal1[1] == '':
                board[diagonal["positions"][2]][diagonal["positions"][3]] = 'X'
            elif diagonal1[2] == '':
                board[diagonal["positions"][4]][diagonal["positions"][5]] = 'X'

    for i in range(3):
        check_row(i)
        check_column(i)

    diagonal1 = {
        "values": [board[0][0], board[1][1], board[2][2]],
        "positions": [0,0,1,1,2,2]
    }
    diagonal2 = {
        "values": [board[0][2], board[1][1], board[2][0]],
        "positions": [0,2,1,1,2,0]
    }
    check_diagonals(diagonal1)
    check_diagonals(diagonal2)


def offensive_moves(board):
    def check_center():
        if board[1][1] == '':
            board[1][1] = 'X'

    def check_corners(rows=[0,2], columns=[0,2]):
        count = 0
        for row in rows:
            if board[row[count]][columns[count]] == '':
                board[row[count]][columns[count]] = 'X'
            elif board[row[count]][columns[count + 1]] == '':
                board[row[count]][columns[count +1]] = 'X'
            elif board[row[count + 1]][columns[count]] == '':
                board[row[count + 1]][columns[count]] = 'X'
            elif board[row[count + 1]][columns[count + 1]] == '':
                board[row[count + 1]][columns[count + 1]] = 'X'

    def check_middles():
        pass




if __name__ == "__main__":
    app.run(debug=True)
