"""
Module for AI opponent.
"""

class AiError(Exception):
    pass

def move(player, board):
    """
    Move according to strategy:
        Win, if able.
        Block opponent from winning, if able.
        Create a fork to guarantee victory, if able.
        Block an opponent from forking by:
            blocking the fork position, if able.
            forcing another move, if able
        Take the center, if able.
        Take the opposite corner from your opponent, if able.
        Take any corner.
        Take any side.
    """
    cur_game = board.game()
    strategy = [win, block, fork, block_fork,
                  center, opposite_corner, any_corner,
                  any_side]

    move = None
    for tactic in strategy:
        if move or not cur_game.turn:
            break
        move = tactic(board)

    if not cur_game.turn:
        return
    if not move:
        print("cur_game.turn: %s" % cur_game.turn)
        raise AiError("Nothing to be done.")
    (x, y) = move
    return cur_game.move(player, x, y)

def winning_move(board, player, format="single"):
    """
    Look for a move that will win the game.  Take it, if one is found.

    """

    cur_game = board.game()
    opponent = cur_game.get_opponent(player)
    opponent_mark = cur_game.get_mark(opponent)
    my_mark = cur_game.get_mark(player)
    paths = board.traverse(banned=[opponent_mark], requires={my_mark: 2})

    return_list = []
    for p in paths:
        for coords in p:
            if board.square(coords) == " ":
                if format == "single":
                    return coords
                else:
                    return_list.append(coords)

    if format == "list":
        return return_list

    return None

def forking_move(board, player, format="single"):
    """
    Look for a move that will result in two possible ways to win,
    guaranteeing victory if the opposition can't win next round.

    """

    cur_game = board.game()
    opponent = cur_game.get_opponent(player)
    opponent_mark = cur_game.get_mark(opponent)
    my_mark = cur_game.get_mark(player)

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
            if board.square(e) == my_mark:
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

    return None

def list_forcing_moves(board, player):
    """
    Return moves that force opponent to move, thus preventing
    him from making a fork you can't block otherwise.

    """

    cur_game = board.game()
    opponent = cur_game.get_opponent(player)
    opponent_mark = cur_game.get_mark(opponent)
    my_mark = cur_game.get_mark(player)
    paths = board.traverse(banned=[opponent_mark], requires={my_mark: 1})

    coord_list = []
    move_list = []
    for e in paths:
        for c in e:
            coord_list.append(c)

    for e in coord_list:
        if board.square(e) != my_mark:
            move_list.append(e)

    return move_list

def win(board):
    """
    Win, if able.

    """
    move = winning_move(board, "ai")
    if move:
        print("FTW!")
    return move

def block(board):
    """
    Block opponent from winning, if able.

    """
    cur_game = board.game()
    move = winning_move(board, cur_game.get_opponent("ai"))
    if move:
        print("OH NO YOU DON'T!")
    return move

#FIXME: Non forks still being considered forks.
def fork(board):
    """
    Create a fork, resulting in multiple ways to win.

    """
    move = forking_move(board, "ai")
    if move:
        print("Fork!")
    return move

def block_fork(board):
    """
    Detect a fork, and block it.

    """
    cur_game = board.game()
    move = None
    player = "ai"
    opponent = cur_game.get_opponent(player)
    forks = forking_move(board, opponent, format="list")
    flen = len(forks)
    if flen == 0:
        return None
    elif flen == 1:
        move = forks[0]
    else:
        #FIXME?: We end up here trying to force moves, but no
        #FIXME?: move is chosen.  A better solution than this
        #FIXME?: may be necessary.
        print("Brute force!")
        force_moves = list_forcing_moves(board, player)
        for e in force_moves:
            (x, y) = e
            import game
            test_board = game.Board(cur_game, setup=board.full())
            test_board = test_board.move(player, x, y, test=True)
            # We've added our move to our temporary board, now check it
            # for forks and wins by our opponent.  The coords that don't
            # result in these to a list.
            test_forks = forking_move(test_board, opponent, format="list")
            for forced_fork in test_forks:
                if forced_fork in force_moves:
                    print("Useless force %s causes fork." % str(e))
                    continue
            test_wins = winning_move(test_board, opponent, format="list")
            for forced_win in test_wins:
                if forced_win in force_moves:
                    print("Useless force %s causes win." % str(e))
                    continue
            move = e
            
        """
        print("force_moves: %s" % force_moves)
        print("useful_moves: %s" % useful_moves)

        from sets import Set
        fork_set = Set(forks)
        force_set = Set(force_moves)
        try:
            # Subtracting the fork set doesn't make sense.
            # It's the OPPONENT we don't want moving there,
            # not us.  We want to move there so we can force
            # his move in addition to mangling his fork options.
            move = list(force_set & fork_set)[0]
        except IndexError:
            pass
        """

    if move:
        print("A FISHFORK IS NO MATCH FOR MY MACHINE.")
    return move

def center(board):
    """
    Claim the center square, if available.

    """

    center = (1, 1)
    if board.square(center) == " ":
        print("The center cannot hold...")
        return (1, 1)
        
    return None

def opposite_corner(board):
    """
    If opponent is in one corner, grab the opposite.

    """
    cur_game = board.game()
    opponent = cur_game.get_opponent("ai")
    opponent_mark = cur_game.get_mark(opponent)
    for corner in [(0, 0), (0, 2),
                   (2, 0), (2, 2)]:
        if board.square(corner) == opponent_mark:
            (x, y) = corner
            x = abs(x - 2)
            y = abs(y - 2)
            if board.square((x, y)) == " ":
                print("Equal and opposite reaction.")
                return (x, y)

    return None
    
def any_corner(board):
    """
    Grab any corner.

    """
    for corner in [(0, 0), (0, 2),
                   (2, 0), (2, 2)]:
        if board.square(corner) == " ":
            print("Corner!")
            return corner

    return None

def any_side(board):
    """
    Grab any middle side space.

    """
    #00 01 02
    #10 11 12
    #20 21 22
    for side in [(0, 1),
          (1, 0),       (1, 2),
                 (2, 1)]:
        if board.square(side) == " ":
            print("Side!")
            return side 

    return None


