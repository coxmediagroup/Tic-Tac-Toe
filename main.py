# Console tic-tac-toe
# Adding a comment to see if I can use git properly.

BLANK = '_'
X = 'X'
O = 'O'
GRID = ['*'] + [BLANK] * 9
LINES = ((1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7), (2, 5, 8), (3, 6, 9), (1, 5, 9), (3, 5, 7))


def check_for_win(player):
    for a, b, c in LINES:
        if player == GRID[a] == GRID[b] == GRID[c]:
            return True
    return False


def print_board():
    print GRID[1], GRID[2], GRID[3]
    print GRID[4], GRID[5], GRID[6]
    print GRID[7], GRID[8], GRID[9]
    print


def get_human_move(human_plays, move_count):
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
    return move, None


def find_winning_move(player):
    for square in range(1, 10):
        if GRID[square] == BLANK:
            GRID[square] = player
            win = check_for_win(player)
            GRID[square] = BLANK
            if win:
                return square
    return None


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


def any_square():
    return GRID.index(BLANK)


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
    msg = 'The computer picks square %d.' % move
    return move, msg


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


def play(player1, player2, verbose=True):
    move_count = 0
    GRID[1:10] = [BLANK] * 9
    while move_count < 9:
        if move_count % 2 == 0:
            move, msg = player1(X, move_count)
            player = X
        else:
            move, msg = player2(O, move_count)
            player = O
        GRID[move] = player
        move_count += 1
        if verbose:
            if msg:
                print msg
            print_board()

        if check_for_win(player):
            return player
    else:
        return BLANK


def main():
    human_plays = print_instructions()
    if human_plays == X:
        winner = play(get_human_move, get_computer_move, verbose=True)
    else:
        winner = play(get_computer_move, get_human_move, verbose=True)
    if winner == human_plays:
        print 'You win!'
    elif winner == BLANK:
        print 'Tie game!'
    else:
        print 'Computer wins!'

if __name__ == '__main__':
    main()