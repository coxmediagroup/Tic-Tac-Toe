true_board = [[None, None, None],
              [None, None, None],
              [None, None, None]]
X = 1
O = 2
TOP_LEFT = 0, 0
TOP_MID = 0, 1
TOP_RIGHT = 0, 2
MID_LEFT = 1, 0
CENTER = 1, 1
MID_RIGHT = 1, 2
BOT_LEFT = 2, 0
BOT_MID = 2, 1
BOT_RIGHT = 2, 2
top_row = None
middle_row = None
bottom_row = None
left_column = None
middle_column = None
right_column = None
left_diagonal = None
right_diagonal = None
state_translation = {'top_row': (TOP_LEFT, TOP_MID, TOP_RIGHT),
                     'middle_row': (MID_LEFT, CENTER, MID_RIGHT),
                     'bottom_row': (BOT_LEFT,BOT_MID, BOT_RIGHT),
                     'left_column': (TOP_LEFT, MID_LEFT, BOT_LEFT),
                     'middle_column': (TOP_MID, CENTER, BOT_MID),
                     'right_column': (TOP_RIGHT, MID_RIGHT, BOT_RIGHT),
                     'left_diagonal': (TOP_LEFT, CENTER, BOT_RIGHT),
                     'right_diagonal': (TOP_RIGHT, CENTER, BOT_LEFT)}


def update_square(player, square):
    true_board[square[0]][square[1]] = player
    build_state(true_board)


def build_state(board):
    global top_row, middle_row, bottom_row
    global left_column, middle_column, right_column
    global left_diagonal, right_diagonal

    top_row = board[0]
    middle_row = board[1]
    bottom_row = board[2]
    left_column = [row[0] for row in board]
    middle_column = [row[1] for row in board]
    right_column = [row[2] for row in board]
    left_diagonal = [board[0][0], board[1][1], board[2],[2]]
    right_diagonal = [board[0][2], board[1][1], board[2][0]]


def test_line(line, positive_result):
    if positive_result == X:
        negative_result = O
    else:
        negative_result = X

    positive_count = 0
    negative_count = 0
    null_count = 0

    for space in line:
        if space == positive_result:
            positive_count += 1
        if space == negative_result:
            negative_count += 1
        if space is None:
            null_count += 1

    return positive_count, negative_count, null_count


def can_player_win(player):
    """Return tuple of winning move or None"""
    if test_line(top_row, player) == (2, 0, 1):
        return state_translation['top_row'][top_row.index(None)]
    if test_line(middle_row, player) == (2, 0, 1):
        return state_translation['middle_row'][middle_row.index(None)]
    if test_line(bottom_row, player) == (2, 0, 1):
        return state_translation['bottom_row'][bottom_row.index(None)]
    if test_line(left_column, player) == (2, 0, 1):
        return state_translation['left_column'][left_column.index(None)]
    if test_line(middle_column, player) == (2, 0, 1):
        return state_translation['middle_column'][middle_column.index(None)]
    if test_line(right_column, player) == (2, 0, 1):
        return state_translation['right_column'][right_column.index(None)]
    if test_line(left_diagonal, player) == (2, 0, 1):
        return state_translation['left_diagonal'][left_diagonal.index(None)]
    if test_line(right_column, player) == (2, 0, 1):
        return state_translation['right_column'][right_column.index(None)]
    return None


def can_player_fork(player):
    test = 2, 1, 0
    left = test_line(left_diagonal, player)
    right = test_line(right_diagonal, player)
    if left == test or right == test:
        return not true_board[1][1] == player
    return False


def is_board_empty():
    """Return boolean"""
    for row in true_board:
        for square in row:
            if square is not None:
                return False

    return True


def is_center_empty():
    """Return boolean"""
    return true_board[1][1] is None


def is_corner_empty():
    """Return list of empty corners"""
    empty_corners = []
    corners = [TOP_LEFT, TOP_RIGHT, BOT_LEFT, BOT_RIGHT]
    for corner in corners:
        if true_board[corner[0]][corner[1]] is None:
            empty_corners.append(corner)

    return empty_corners


def empty_sides():
    """Return list of empty corners"""
    empty_sides_list = []
    sides = [TOP_MID, MID_LEFT, MID_RIGHT, BOT_MID]
    for side in sides:
        if true_board[side[0]][side[1]] is None:
            empty_sides_list.append(corner)

    return empty_sides_list