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
    board_instance = Board(board)
    board_instance.prioritize_moves()
    board = board_instance.new_board

    return jsonify(board=board, is_winner=board_instance.is_winner)
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
            [(0, 1, board[0][1]), (1, 1, board[1][1]), (2, 1, board[2][1])],
            [(0, 2, board[0][2]), (1, 2, board[1][2]), (2, 2, board[2][2])],
            [(0, 0, board[0][0]), (1, 1, board[1][1]), (2, 2, board[2][2])],
            [(0, 2, board[0][2]), (1, 1, board[1][1]), (2, 0, board[2][0])]
        ]
        self.ranked_triplets = []
        self.corners = [(0, 0), (0, 2), (0, 2), (2, 2)]
        self.new_board = board
        self.is_winner = False
        self.player_letter = 'O'
        self.computer_letter = 'X'

    def prioritize_moves(self):
        """
        Loop through rows, columns and diagonals to find plays
        """
        for triplet in self.orig_board:
            self.ranked_triplets += self.tally_values(triplet)

        sorted_list = sorted(self.ranked_triplets)

        if len(sorted_list) > 0:
            ranking, (x, y) = sorted_list.pop()
            self.new_board[x][y] = 'X'
        else:
            pass

    def tally_values(self, triplet):
        """
        Assign rank to valid plays if there are any.
        10 - winning
        9 - blocking player's win
        8 - take middle square
        7 - take corner
        6 - take other square
        """

        # Readability won out over optimization
        playable_squares = [(x, y) for x, y, value in triplet if value == '']
        playable_corners = [(x, y) for x, y in playable_squares if (x, y) in self.corners]
        can_win = sum([1 for x, y, value in triplet if value == self.computer_letter]) == 2
        can_lose = sum([1 for x, y, value in triplet if value == self.player_letter]) == 2
        can_take_middle = True if triplet[1] == (1, 1, '') else False

        ranked_triplets = []

        if len(playable_squares) == 0:
            pass
        else:
            if can_win:
                ranked_triplets.append((10, playable_squares[0]))
                self.is_winner = True
            elif can_lose:
                ranked_triplets.append((9, playable_squares[0]))
            elif can_take_middle:
                ranked_triplets.append((8, (1, 1)))
            elif len(playable_corners) > 0:
                for corner in playable_corners:
                    ranked_triplets.append((7, corner))
            else:
                for square in playable_squares:
                    ranked_triplets.append((6, square))

        return ranked_triplets

if __name__ == "__main__":
    app.run(debug=True)
