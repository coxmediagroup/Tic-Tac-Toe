"""
Module for AI opponent.
"""

def move(game):
    """
    Move randomly for now.
    """
    move = winning_move(game)
    if not move:
        move = random_move(game)
    (x, y) = move
    return game.move(ai, x, y)

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
    paths = game.traverse_board()

    # This won't work, and it isn't a good way to do this.
    # alter game.traverse_board() to allow pathway selection.
    for e in paths:
        if((self.square_lookup(e[0])
            == self.square_lookup(e[1])
            == self.square_lookup(e[2]))
           and self.square_lookup(e[0]) != " "):
            winner = self.square_lookup(e[0])
            break

