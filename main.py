# Console tic-tac-toe
# Adding a comment to see if I can use git properly.

BLANK = '_'
X = 'X'
O = 'O'
GRID = [BLANK] * 10
LINES = ((1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7), (2, 5, 8), (3, 6, 9), (1, 5, 9), (2, 5, 8))
MOVE_COUNT = 0


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


def get_human_move(human_plays, first=False):
    move = None
    while move is None:
        response = raw_input('Enter your move (1-9): ').lower()
        if response == 'quit':
            move = 'quit'
        elif response == 'pass':
            if first:
                print 'OK, I will go first.'
                move = 'pass'
            else:
                print 'You may only pass on your first move.'
        else:
            if len(response) == 1 and '1' <= response <= '9':
                square = int(response)
                if GRID[square] == BLANK:
                    move = square
                else:
                    print 'That square is occupied.'
            else:
                print 'Illegal move.'
    assert move is not None
    return move


def find_winning_move(player):
    for square in range(1,10):
        if GRID[square] == BLANK:
            GRID[square] = player
            win = check_for_win(player)
            GRID[square] = BLANK
            if win:
                return square
    return None


def find_double_attack(player):
    move = None
    for square in range(1,10):
        if GRID[square] == BLANK:
            GRID[square] = player
            attacks = 0
            for a, b, c in LINES:
                if (GRID[a], GRID[b], GRID[c]) in [(player, player, BLANK), (player, BLANK, player),
                                                   (BLANK, player, player)]:
                    attacks += 1
                    if attacks == 2:
                        move = square
                        break
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
        elif move_count == 1:
            if GRID[5] == O: # Only safe move for human player
                move = 9
            elif GRID[4] == O or GRID[7] == O or GRID[8] == O:
                move = 3
            else:
                move = 7
        else:
            move = find_winning_move(X) or find_winning_move(O) or find_double_attack(X)
            move = move or find_double_attack(O) or any_square()
    else:
        if move_count == 0:
            if GRID[5] == X:
                move = 1
            else:
                move = 5
        elif move_count == 1:
            move = find_winning_move(X)
            if move is None:
                if GRID[5] == X:
                    move = 3
                elif (GRID[1] == GRID[9] == X) or (GRID[3] == GRID[7] == X):
                    move = 2
                else:
                    move = find_double_attack(O) or find_double_attack(X) or any_square()
        else:
            move = find_winning_move(O) or find_winning_move(X) or find_double_attack(O)
            move = move or find_double_attack(X) or any_square()

    print 'The computer picks square %d.' % move
    return move


def print_instructions():
    print 'Play tic-tac-toe against the computer. You know the rules.'
    print 'The squares are numbered 1-9. To move, type the number of your square.'
    print 'If you would like to play second, type "pass" (without quotes).'
    print 'If you would like to quit, type "quit" (without quotes).'
    print


def main():
    human_plays = X
    computer_plays = O
    print_instructions()
    human_move = get_human_move(human_plays, first=True)
    if human_move == 'quit':
        return None
    if human_move == 'pass':
        human_plays = O
        computer_plays = X
    else:
        GRID[human_move] = human_plays
        print_board()
    for move_count in range(4):
        computer_move = get_computer_move(computer_plays, move_count)
        GRID[computer_move] = computer_plays
        print_board()
        if check_for_win(computer_plays):
            print 'The computer won! All hail the computer!'
            break
        human_move = get_human_move(human_plays)
        if human_move == 'quit':
            break
        GRID[human_move] = human_plays
        print_board()
        if check_for_win(human_plays):
            print 'You won!'
            break
    else:
        print 'The game is a draw!'

if __name__ == '__main__':
    main()