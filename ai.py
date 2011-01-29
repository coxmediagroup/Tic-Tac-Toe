"""
Module for AI opponent.
"""

def move(game):
    """
    Move randomly for now.
    """
    print("Win?")
    move = winning_move(game)
    if not move:
        move = random_move(game)
    (x, y) = move
    return game.move("ai", x, y)

#FIXME: DELETE ME
def random_move(game):
    """
    Move randomly.  Doesn't even check for valid moves.
    
    """
    import random
    move = (random.randrange(0, 3), random.randrange(0, 3))
    return move

def winning_move(game):
    """
    Look for a move that will win the game.  Take it, if one is found.
    """
    paths = game.traverse_board(banned=["X"])
    print("BOARD:" + repr(paths))

    # This won't work, and it isn't a good way to do this.
    # alter game.traverse_board() to allow pathway selection.
    """
    for e in paths:
        if((game.square_lookup(e[0])
            == game.square_lookup(e[1])
            == game.square_lookup(e[2]))
           and game.square_lookup(e[0]) != " "):
            winner = game.square_lookup(e[0])
            break
    """
    return False

