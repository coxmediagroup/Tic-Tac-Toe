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
        self.new_board = board
        self.player_letter = 'O'
        self.computer_letter = 'X'

    # Moves & values:
    # 1 - winning
    # 2 - blocking player's win
    # 3 - take middle square
    # 4 - take corner
    # 5 - take other square

    def prioritize_moves(self):
        for triplet in orig_board:
            ranking = 0
            ranking += tally_values(ranking, triplet, computer_letter)
            ranking += tally_values(ranking, triplet, player_letter)

            self.ranked_triplets.append([ranking, triplet])

        make_play()

        def tally_values(ranking, triplet, letter):
            count = 0
            corners = [(0,0), (0,2), (0,2), (2,2)]

            for index, square in enumerate(triplet):
                xy = (square[0], square[1])

                if square[2] == letter:
                    count += 1

                if square[2] == '':
                    # If this is the middle square, make it worth more than corners
                    if xy == (1,1):
                        ranking += 2

                    if xy in corners:
                        ranking += 1

            # If someone can win, rank higher
            if count == 2:
                ranking += 1

                # If computer can win, rank higher
                if letter == computer_letter:
                    ranking += 1

            return ranking

    return self.new_board

if __name__ == "__main__":
    app.run(debug=True)
