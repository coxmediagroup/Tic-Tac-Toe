"""
Module for AI opponent.
"""

def move(game):
    """
    Move randomly for now.
    """
    print("Win?")
    move = win(game)
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
    mark = game.get_mark(opponent)
    paths = game.traverse_board(banned=[mark], min=2)

    for p in paths:
        for coords in p:
            if game.square_lookup(coords) == " ":
                print("FTW!")
                return coords
    return False

def win(game):
    move = winning_move(game, "ai")
    return move
