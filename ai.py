"""
Module for AI opponent.

"""

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

    strategy= [center]

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
    pass
