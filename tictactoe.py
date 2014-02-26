from sys import maxsize
###
#
# Assuming the structure
# 
# 0 | 1 | 2
# ---------
# 3 | 4 | 5
# ---------
# 6 | 7 | 8
#
###

PLAYER_X = 1            # The maximizing player
DRAW = 0
PLAYER_0 = -1           # The minimizing player


def check_win(board):
    # check columns
    for space in range(3):
        if board[space] == board[space+3] and board[space] == board[space+6]:
            if board[space] == "X" or board[space] == "O":
                return True, board[space]

    # check rows
    for space in (0, 3, 6):
        if board[space] == board[space+1] and board[space] == board[space+2]:
            if board[space] == "X" or board[space] == "O":
                return True, board[space]

    # check diags
    if board[0] == board[4] and board[0] == board[8]:
            if board[0] == "X" or board[0] == "O":
                return True, board[0]

    if board[2] == board[4] and board[2] == board[6]:
            if board[2] == "X" or board[2] == "O":
                return True, board[2]

    return (False, None)


def normalize_position(position):
    pos = int(position) - 1
    if pos <= 8 and pos >= 0:
        return pos
    return False


def is_available_position(board, position):
    if board[position] != "X" or board[position] != "O":
        return True
    return False


def write_board(board):
    print ""
    print "        %s | %s | %s" % (board[0], board[1], board[2])
    print "        ---------"
    print "        %s | %s | %s" % (board[3], board[4], board[5])
    print "        ---------"
    print "        %s | %s | %s" % (board[6], board[7], board[8])
    print ""


def generate_move(board, move):
    if len(set(board)) == 1:    # assuming alternating moves
        return DRAW, 4

    if move == "O":
        next_move = "X"
    else:
        next_move = "O"

    won, winner = check_win(board)
    if won:
        if winner == "O":
            return PLAYER_0, -1
        else:
            return PLAYER_X, -1

    X_count = board.count("X")
    O_count = board.count("O")
    if X_count + O_count == 9:
        return DRAW, -1

    possible_positions = [] # list for appending the result
    temp_board = [] # list for storing the indexes where '-' appears
    for i in range(len(board)):
        if board[i] != "X" and board[i] != "O":
            temp_board.append(i)

    for i in temp_board:
        board[i] = move
        r, m = generate_move(board, next_move)
        possible_positions.append(m)
        board[i] = "%s" % str(i + 1)

    if len(possible_positions):    # return terminal state
        if move is "O":
            min_move = min(possible_positions)
            return min_move, temp_board[possible_positions.index(min_move)]
        else:
            max_move = max(possible_positions)
            return max_move, temp_board[possible_positions.index(max_move)]


if __name__ == "__main__":
    # initial board
    board = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    game_over = False
    plays = 0
    print " ------------ ---- ----------  ------------ --------- ----------  ------------ --------- ----------"
    print " |          | |  | |        |  |          | |  ---  | |        |  |          | |  ---  | |        |"
    print " ----    ---- |  | |  -------  ----    ---- |  | |  | |  -------  ----    ---- |  | |  | |  -------"
    print "     |  |     |  | |  |            |  |     |  ---  | |  |            |  |     |  | |  | |        |"
    print "     |  |     |  | |  -------      |  |     |  | |  | |  -------      |  |     |  | |  | |  -------"
    print "     |  |     |  | |        |      |  |     |  | |  | |        |      |  |     |  ---  | |        |"
    print "     ----     ---- ----------      ----     ---- ---- ----------      ----     --------- ----------"
    print "                                                                                                   "
    print "                                                                                                   "
    print "                                                                                                   "
    print "Rules:"
    print " * You are 'X'"
    print " * The computer is 'O'"
    print " * You will lose"
    print ""
    print "Begin!"
    print ""
    print "Pick a spot (available spots are numbered)"
    write_board(board)
    while not game_over:
        player_position = raw_input("Your position: ")
        position = normalize_position(player_position)
        available = is_available_position(board, position)
        if type(position) is int and available:
            board[position] = "X"
            win, winner = check_win(board)
            if win:
                print "WE HAVE A WINNER: %s" % winner
                print ""
                print "%s wins after %d plays." % (winner, plays)
                game_over = True
                break
            plays += 1
            if plays == 9:
                print "NO WINNER"
                print ""
                print "The game is a draw."
                game_over = True
                break
            write_board(board)
            print "Computer is moving..."
            val, computer_position = generate_move(board, "O")
            board[computer_position] = "O"
            win, winner = check_win(board)
            if win:
                print "WE HAVE A WINNER: %s" % winner
                print ""
                print "%s wins after %d plays." % (winner, plays)
                game_over = True
                break
            else:
                write_board(board)
            plays += 1
            if plays == 9:
                print "NO WINNER"
                print ""
                print "The game is a draw."
                game_over = True
                break
        else:
            print "Position not available. Try again."
