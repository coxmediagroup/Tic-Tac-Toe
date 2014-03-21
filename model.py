board = [[None, None, None],
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
    board[square[0]][square[1]] = player
    build_state()


def build_state():
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