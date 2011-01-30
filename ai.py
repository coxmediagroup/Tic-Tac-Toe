"""
Module for AI opponent.
"""

class AiError(Exception):
    pass

def move(game):
    """
    Move according to strategy:
        Win, if able.
        Block opponent from winning, if able.
        Create a fork to guarantee victory, if able.
        Block an opponent from forking by:
            forcing another move, if able
            blocking the fork position, if able.
        Take the center, if able.
        Take the opposite corner from your opponent, if able.
        Take any corner.
        Take any side.
    """
    strategy = [win, block, fork, block_fork,
                  center, opposite_corner, any_corner,
                  any_side]

    move = None
    for tactic in strategy:
        if move or not game.turn:
            break
        move = tactic(game)

    if not game.turn:
        return
    if not move:
        print("game.turn: %s" % game.turn)
        raise AiError("Nothing to be done.")
    (x, y) = move
    return game.move("ai", x, y)

def winning_move(game, player):
    """
    Look for a move that will win the game.  Take it, if one is found.

    """

    opponent = game.get_opponent(player)
    opponent_mark = game.get_mark(opponent)
    my_mark = game.get_mark(player)
    paths = game.traverse_board(banned=[opponent_mark], requires={my_mark: 2})

    for p in paths:
        for coords in p:
            if game.square_lookup(coords) == " ":
                return coords
    return False

def forking_move(game, player, format="single"):
    """
    Look for a move that will result in two possible ways to win,
    guaranteeing victory if the opposition can't win next round.

    """

    opponent = game.get_opponent(player)
    opponent_mark = game.get_mark(opponent)
    my_mark = game.get_mark(player)

    # Get a list of paths that have 1 move taken, unblocked by opponent.
    paths = game.traverse_board(banned=[opponent_mark], requires={my_mark: 1})

    # Pathways are irrelevent, make one list.
    coord_list = []
    for e in paths:
        for c in e:
            coord_list.append(c)

    # Intersect them, checking for overlapping coordinates.
    coords = {}
    for e in coord_list:
        if e not in coords.keys():
            # Because of the way traverse_board slices the board,
            # moves intersect with themselves, leading to strange math.
            # Delete them, compare only spaces from this point forward.
            if game.square_lookup(e) == my_mark:
                continue

            # We're tracking intersections, not numbers,
            # so start with 0.
            coords[e] = 0
        else:
            coords[e] += 1

    # Pick the most vicious fork possible.  I.e., most intersections.
    max = 0
    for e in coords.keys():
        max = coords[e] if coords[e] > max else max

    # If max is not > 0, then there aren't any interesting
    # intersections.
    return_list = []
    if max > 0:
        for e in coords.keys():
            if coords[e] == max:
                # We're indexing by coords, so just return e.
                if format == "single":
                    return e
                elif format == "list":
                    return_list.append(e)

    if format == "list":
        return return_list

    #FIXME: Why do you keep returning False?  Doesn't it make
    #FIXME: more sense to return None?  Look into it.
    return False

def list_forcing_moves(game, player):
    """
    Return moves that force opponent to move, thus preventing
    him from making a fork you can't block otherwise.

    """

    opponent = game.get_opponent(player)
    opponent_mark = game.get_mark(opponent)
    my_mark = game.get_mark(player)
    paths = game.traverse_board(banned=[opponent_mark], requires={my_mark: 1})

    coord_list = []
    move_list = []
    for e in paths:
        for c in e:
            coord_list.append(c)

    for e in coord_list:
        if game.square_lookup(e) != my_mark:
            move_list.append(e)

    return move_list

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

def fork(game):
    """
    Create a fork, resulting in multiple ways to win.

    """
    move = forking_move(game, "ai")
    if move:
        print("Fork!")
    return move

def block_fork(game):
    """
    Detect a fork, and block it.

    """
    #FIXME?  Block fork may be out of order.  force first, block fork after.
    move = None
    forks = forking_move(game, game.get_opponent("ai"), format="list")
    flen = len(forks)
    if flen == 0:
        return False
    elif flen == 1:
        move = forks[0]
    else:
        print("Brute force!")
        force_moves = list_forcing_moves(game, "ai")
        from sets import Set
        fork_set = Set(forks)
        force_set = Set(force_moves)
        try:
            move = list(force_set - fork_set)[0]
        except IndexError:
            pass

    if move:
        print("A FISHFORK IS NO MATCH FOR MY MACHINE.")
    return move

def center(game):
    """
    Claim the center square, if available.
    """

    center = (1, 1)
    if game.square_lookup(center) == " ":
        print("The center cannot hold...")
        return (1, 1)
        
    return False

def opposite_corner(game):
    """
    If opponent is in one corner, grab the opposite.

    """
    opponent = game.get_opponent("ai")
    opponent_mark = game.get_mark(opponent)
    for corner in [(0, 0), (0, 2),
                   (2, 0), (2, 2)]:
        if game.square_lookup(corner) == opponent_mark:
            (x, y) = corner
            x = abs(x - 2)
            y = abs(y - 2)
            if game.square_lookup((x, y)) == " ":
                print("Equal and opposite reaction.")
                return (x, y)

    return False
    
def any_corner(game):
    """
    Grab any corner.

    """
    for corner in [(0, 0), (0, 2),
                   (2, 0), (2, 2)]:
        if game.square_lookup(corner) == " ":
            print("Corner!")
            return corner

    return False

def any_side(game):
    """
    Grab any middle side space.

    """
    #00 01 02
    #10 11 12
    #20 21 22
    for side in [(0, 1),
          (1, 0),       (1, 2),
                 (2, 1)]:
        if game.square_lookup(side) == " ":
            print("Side!")
            return side 

    return False


