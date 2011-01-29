"""
Module for AI opponent.
"""

def move(game):
    """
    Move randomly for now.
    """
    move = win(game)
    if not move:
        move = block(game)
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

def winning_move(game, player):
    """
    Look for a move that will win the game.  Take it, if one is found.
    """

    opponent = game.get_opponent(player)
    opponent_mark = game.get_mark(opponent)
    my_mark = game.get_mark(player)
    blank = " "
    paths = game.traverse_board(banned=[opponent_mark], requires={my_mark: 2})

    for p in paths:
        for coords in p:
            if game.square_lookup(coords) == " ":
                print("Win condition for: %s" % player)
                return coords
    return False

def win(game):
    """
    Win, if able.

    """
    move = winning_move(game, "ai")
    if move:
        print("FTW!")
    return move

def block(game):
    """
    Block opponent from winning, if able.

    """
    move = winning_move(game, game.get_opponent("ai"))
    if move:
        print("OH NO YOU DON'T!")
    return move
