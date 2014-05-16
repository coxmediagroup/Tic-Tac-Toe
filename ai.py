"""
Module for AI opponent.

"""

class AiError(Exception):
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

    strategy= [win, fork, center, opposite_corner, any_corner, any_side]

    move = None
    for tactic in strategy:
        if move:
            break
        move = tactic(board)

    if not move:
        raise AiError("Nothing to be done.")

    board.move(move, "O")

def center(board):
    """
    Claim the center square, if available.

    """

    center = (1, 1)
    if board.square(center) == " ":
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
    move = winning_move(board, "O")
    return move

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

    # Pick the most vicious fork possible (.e., most interesections.)
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

    move = forking_move(board, "O")
    return move
