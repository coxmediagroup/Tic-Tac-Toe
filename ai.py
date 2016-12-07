"""
Module for AI opponent.

"""

class AiError(Exception):
    """
    Exception for when the AI can't figure out what to do.

    """
    pass

def move(board):
    """
    Move according to strategy:
        Win, if able.
        Block opponent from winning, if able.
        Create a fork to guarantee victory, if able.
        Block an opponent from forking by:
            blocking the fork position, if able.
            forcing another move, if able.
        Take the center, if able.
        Take the opposite corner from your opponent, if able.
        Take any corner.
        Take any side.

    """

    strategy = [win, block, fork, block_fork, center, opposite_corner,
                any_corner, any_side]

    move_ = None
    for tactic in strategy:
        if move_:
            break
        move_ = tactic(board)

    if not move_:
        raise AiError("Nothing to be done.")

    board.move(move_, "O")

def center(board):
    """
    Claim the center square, if available.

    """

    center_ = (1, 1)
    if board.square(center_) == " ":
        return (1, 1)

    return None

def opposite_corner(board):
    """
    If opponent is in one corner, grab the opposite.

    """

    opponent_mark = "X"
    for corner in [(0, 0), (0, 2),
                   (2, 0), (2, 2)]:
        if board.square(corner) == opponent_mark:
            (x, y) = corner
            x = abs(x - 2)
            y = abs(y - 2)
            if board.square((x, y)) == " ":
                return (x, y)

    return None

def any_corner(board):
    """
    Grab any corner.

    """
    for corner in [(0, 0), (0, 2),
                   (2, 0), (2, 2)]:
        if board.square(corner) == " ":
            return corner

    return None

def any_side(board):
    """
    Grab any middle side space.

    """

    #00 01 02
    #10 11 12
    #20 21 22

    for side in [(0, 1), (1, 0),
                 (1, 2), (2, 1)]:
        if board.square(side) == " ":
            return side

    return None

def winning_move(board, symbol, return_format="single"):
    """
    Look for a move that will win the game.  Take it, if found.

    """
    opponent_mark = "X" if symbol == "O" else "O"
    my_mark = symbol
    paths = board.traverse(banned=[opponent_mark], requires={my_mark: 2})

    return_list = []
    for p in paths:
        for coords in p:
            if board.square(coords) == " ":
                if return_format == "single":
                    return coords
                else:
                    return_list.append(coords)

    if return_format == "list":
        return return_list

    return None

def win(board):
    """
    Win, if able.

    """
    move_ = winning_move(board, "O")
    return move_

def forking_move(board, symbol, return_format="single"):
    """
    Look for a move that will result in two possible ways to win,
    guaranteeing victory if the opposition can't win next round.

    """
    my_mark = symbol
    opponent_mark = "O" if symbol == "X" else "X"

    # Get a list of paths that have 1 move taken, unblocked by opponent.
    paths = board.traverse(banned=[opponent_mark], requires={my_mark: 1})

    # Pathways are irrelevent, make one list.
    coord_list = []
    for e in paths:
        for c in e:
            coord_list.append(c)

    # Intersect them, checking for overlapping coordinates.
    coords = {}
    for e in coord_list:
        if e not in coords.keys():
            # Because of the way Board.traverse slices the board,
            # moves intersect with themselves, leading to strange math.
            # Delete them, compare only spaces from this point forward.
            if board.square(e) in [my_mark, opponent_mark]:
                continue

            # We're tracking intersections, not numbers, so start with 0.
            coords[e] = 0
        else:
            coords[e] += 1

    # Pick the most vicious fork possible (i.e., the most interesections).
    max_ = 0
    for e in coords.keys():
        max_ = coords[e] if coords[e] > max_ else max_

    # If max is not > 0, then there aren't any interesting intersections.
    return_list = []
    if max_ > 0:
        for e in coords.keys():
            if coords[e] == max_:
                # We're indexing by coords, so just return e.
                if return_format == "single":
                    return e
                elif return_format == "list":
                    return_list.append(e)

    if return_format == "list":
        return return_list

    return None

def fork(board):
    """
    Create a fork, resulting in multiple ways to win.

    """

    move_ = forking_move(board, "O")
    return move_

def block(board):
    """
    Block opponent from winning, if able.

    """
    move_ = winning_move(board, "X")
    return move_

def list_forcing_moves(board, player_mark):
    """
    return moves that force opponent to move, thus preventing him from making
    a fork you can't block otherwise.

    """

    my_mark = player_mark
    opponent_mark = "X" if player_mark == "O" else "O"
    paths = board.traverse(banned=[opponent_mark], requires={my_mark: 1})

    coord_list = []
    move_list = []
    for e in paths:
        for c in e:
            coord_list.append(c)

    for e in coord_list:
        if board.square(e) not in [my_mark, opponent_mark]:
            move_list.append(e)

    return move_list

def block_fork(board):
    """
    Detect a fork and block it.

    """

    forks = forking_move(board, "X", return_format="list")
    flen = len(forks)
    move_ = None
    if flen == 0:
        return None
    elif flen == 1:
        move_ = forks[0]
    else:
        force_moves = list_forcing_moves(board, "O")
        for e in force_moves:
            import game
            (x, y) = e
            test_board = game.Board(setup=board.board())
            test_board = test_board.move((x, y), "O", test=True)
            # We've added our move to our temporary board, now check it
            # for forks and wins by our opponent.  The coords that don't
            # result in these, store in a list.
            test_forks = forking_move(test_board, "X", return_format="list")

            new_forks = list(set(test_forks) - set(forks))
            if new_forks:
                continue

            test_wins = winning_move(test_board, "X", return_format="list")
            if test_wins:
                continue

            # Make sure the move we are forcing will actually help us block
            # the fork.  I.e., don't force them to take the fork we're trying
            # to block.
            bad_move = False
            forced_moves = winning_move(test_board, "O", return_format="list")
            for forced_move in forced_moves:
                if forced_move in test_forks:
                    bad_move = True

            if bad_move:
                continue

            move_ = e

    return move_


