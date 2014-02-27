from math import pow

board = [[" "," "," "],[" "," "," "],[" "," "," "],]

def get_open_spaces(board):
    spaces = []
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if (board[i][j] == " "):
                spaces.append([i,j])
    return spaces

print "Let's play Tic Tac Toe"

def setup_players():
    valid_setup = False
    while not valid_setup:
        plr = raw_input("Enter player type (x or o): ")
        if plr.lower() != "x" and plr.lower() != "o":
            print "Invalid player type! Please type \"x\" or \"o\""
        elif plr.lower() == "x":
            com = "o"
            valid_setup = True
        elif plr.lower() == "o":
            com = "x"
            valid_setup = True


plr = "x"
com = "o"
winner = None

def print_board(b):
    print " ", " ", "1", " ", "2", " ", "3"
    print "1 |", b[0][0], "|", b[0][1], "|", b[0][2], "|"
    print "2 |", b[1][0], "|", b[1][1], "|", b[1][2], "|"
    print "3 |", b[2][0], "|", b[2][1], "|", b[2][2], "|"
    print " ", "-" * 13

def check_win(b):
    """
    Checks the state of the board to see if there is a winner or not.
    """
    # Horizontals
    if b[0][0] == b[0][1] == b[0][2] != " ":
        return b[0][0]
    if b[1][0] == b[1][1] == b[1][2] != " ":
        return b[1][0]
    if b[2][0] == b[2][1] == b[2][2] != " ":
        return b[2][0]

    # Verticals
    if b[0][0] == b[1][0] == b[2][0] != " ":
        return b[0][0]
    if b[0][1] == b[1][1] == b[2][1] != " ":
        return b[0][1]
    if b[0][2] == b[1][2] == b[2][2] != " ":
        return b[0][2]

    # Diagonals
    if b[0][0] == b[1][1] == b[2][2] != " ":
        return b[0][0]
    if b[0][2] == b[1][1] == b[2][0] != " ":
        return b[0][2]

    for row in b:
        for col in row:
            # if any square is blank, there is no tie
            if col == " ":
                return None

    # Catch All for tie
    return "-"

def request_move(b):
    row = None
    col = None
    valid_move = False
    while not valid_move:
        try:
            row = int(raw_input("Guess Row:")) - 1
            if row < 0 or row > 2:
                raise Exception("Invalid row given!")
            col = int(raw_input("Guess Col:")) - 1
            if col < 0 or col > 2:
                raise Exception("Invalid col given!")
        except ValueError as e:
            print "That's not a valid number!"
            continue
        except Exception as e:
            print e
            continue
        if b[row][col] == " ":
            valid_move = True
        else:
            print "Invalid move!"
    return (row, col)

def move(row, col, p, b):
    b[row][col] = p

setup_players()
while not winner:
    print_board(board)
    plr_move = request_move(board)
    move(plr_move[0], plr_move[1], plr, board)
    winner = check_win(board)

print print_board(board)
