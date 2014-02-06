# Console Tic-Tac-Toe. This program includes an expert system that cannot be defeated at Tic-Tac-Toe.

# GRID is a list of 10 characters representing the board as follows:
#    1  2  3
#    4  5  6
#    7  8  9
# The element in position zero is ignored.

# The characters for BLANK, X, and O can be changed at will, as long as they are distinct.
# Changing these symbols affects how the board is displayed, but nothing else.

BLANK = '_'
X = 'X'
O = 'O'
GRID = ['*'] + [BLANK] * 9

VERBOSE = True  # Setting this variable to False will suppress mose output.


# Suppresses output for purposes of automated testing.
def silence():
    global VERBOSE
    VERBOSE = False

# LINES describes all possible ways to get three in a row in Tic-Tac-Toe: horizontal, vertical, and diagonal lines.
# This could be changed if you wanted to experiment with variants of Tic-Tac-Toe.

LINES = ((1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7), (2, 5, 8), (3, 6, 9), (1, 5, 9), (3, 5, 7))


# Check whether the indicated player (X or O) has won the game. Returns True or False.
def check_for_win(player):
    for a, b, c in LINES:
        if player == GRID[a] == GRID[b] == GRID[c]:
            return True
    return False


# Displays the current state of the board.
def print_board():
    print GRID[1], GRID[2], GRID[3]
    print GRID[4], GRID[5], GRID[6]
    print GRID[7], GRID[8], GRID[9]
    print


# Prompt the player to make a legal move. Returns an integer between 1 and 9 inclusive.
# The arguments are not used. They are included because the function is passed to the
# 'play' function to select a move, and other move-selection functions require these
# arguments. The second return value is a message to be displayed by the calling function;
# its value is None because no such message should be displayed.

def get_human_move(x, y):
    move = None
    while move is None:
        response = raw_input('Enter your move (1-9): ')
        if len(response) == 1 and '1' <= response <= '9':
            square = int(response)
            if GRID[square] == BLANK:
                move = square
            else:
                print 'That square is occupied.'
        else:
            print 'Illegal move.'
    return move


# Returns a winning move for the player (X or O) if possible.
# Output is an integer between 1 and 9, or None if no winning move is available.
# This function is also used to block the player's opponent.
def find_winning_move(player):
    for square in range(1, 10):
        if GRID[square] == BLANK:
            GRID[square] = player
            win = check_for_win(player)
            GRID[square] = BLANK
            if win:
                return square
    return None


# Find a move for the player (or his opponent) that threatens a win along two different lines.
def find_double_attack(player):
    move = None
    for square in range(1, 10):
        if GRID[square] == BLANK:
            GRID[square] = player
            attacks = False
            for a, b, c in LINES:
                if (GRID[a], GRID[b], GRID[c]) in [(player, player, BLANK), (player, BLANK, player),
                                                   (BLANK, player, player)]:
                    if attacks:
                        move = square
                        break
                    attacks = True
            GRID[square] = BLANK
            if move is not None:
                break
    return move


# Return any available blank square. Presently it returns the first available blank square,
# but it could be modified to return a random blank square.
def any_square():
    return GRID.index(BLANK)


# This is our expert system for selecting moves in Tic-Tac-Toe.
# The arguments 'computer_plays' indicates whether the computer is playing X or O.
# The argument 'move_count' indicates the number of moves that were made previously.
# The function returns two values:
#   - The first value is an integer 1-9 indicating the computer's move.
#   - The second value is a string to be displayed by the calling function.
#
# The strategy for X is as follows:
#   1. On the first move, select the upper left corner
#   2. If O plays to the center, select the lower right corner.
#       - Get 3 in a row if possible, block if necessary. Game will end in a tie unless O makes a mistake.
#   3. If O does not play to the center, choose another corner that threatens 3 in a row horizontally or vertically.
#       - On the next move, we can launch a double attack to win the game.
# The strategy for O is as follows:
#   1. On the first move, select the center square. If the center square is taken, select the upper left corner.
#   2. On subsequent moves, get 3 in a row if possible, and block if necessary.
#       - If X played to opposite corners in his first two moves, then choose a side square.
#       - Threaten a double attack, or block the opponent's double attack.
#       - If all else fails, select the first unoccupied square.

def get_computer_move(computer_plays, move_count):
    if computer_plays == X:
        if move_count == 0:
            move = 1
        elif move_count == 2:
            if GRID[5] == O:     # Only safe move for human player
                move = 9
            elif GRID[4] == O or GRID[7] == O or GRID[8] == O:
                move = 3
            else:
                move = 7
        else:
            move = (find_winning_move(X) or find_winning_move(O) or find_double_attack(X)
                    or find_double_attack(O) or any_square())
    else:
        if move_count == 1:
            if GRID[5] == X:
                move = 1
            else:
                move = 5
        elif move_count == 3:
            move = find_winning_move(X)
            if move is None:
                if GRID[5] == X:
                    move = 3
                elif (GRID[1] == GRID[9] == X) or (GRID[3] == GRID[7] == X):
                    move = 2
                else:
                    move = find_double_attack(O) or find_double_attack(X) or any_square()
        else:
            move = (find_winning_move(O) or find_winning_move(X) or find_double_attack(O) or
                    find_double_attack(X) or any_square())
    if VERBOSE:
        print 'The computer picks square %d.' % move
    return move


# Display the instructions and ask the human if he would like to play X or O.
def print_instructions():
    print 'Play tic-tac-toe against the computer. You know the rules.'
    print 'The squares are numbered 1-9. To move, type the number of your square.'
    print '   1 2 3'
    print '   4 5 6'
    print '   7 8 9'
    print
    while True:
        response = raw_input('Do you wish to play X or O? ').upper()
        if response == 'X' or response == 'O':
            return response
        print 'Please type X or O.'


# Play a game of Tic-Tac-Toe. The required arguments 'player1' and 'player2' are functions that are called
# by 'play' to select moves for X and O respectively. If the optional argument 'verbose' is set to False
# then the output of the functions 'player1' and 'player2' is not displayed. This is useful for testing, but
# we prefer the default verbose=True for interactive play.
#
# The function returns X if X wins, O if O wins, and BLANK if the game is tied.
def play(player1, player2):
    move_count = 0
    GRID[1:10] = [BLANK] * 9
    while move_count < 9:
        if move_count % 2 == 0:
            move = player1(X, move_count)
            player = X
        else:
            move = player2(O, move_count)
            player = O
        GRID[move] = player
        move_count += 1
        if VERBOSE:
            print_board()
        if check_for_win(player):
            return player
    else:
        return BLANK


# Play an interactive game of Tic-Tac-Toe.
def main():
    human_plays = print_instructions()
    if human_plays == X:
        winner = play(get_human_move, get_computer_move)
    else:
        winner = play(get_computer_move, get_human_move)
    if winner == human_plays:
        print 'You win!'
    elif winner == BLANK:
        print 'Tie game!'
    else:
        print 'Computer wins!'

if __name__ == '__main__':
    main()
