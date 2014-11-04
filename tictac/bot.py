"""
    Tic Tac Toe AI

    Each move is evaluated on the following priorities:

    1.)  Win the game.
    2.)  Don't lose the game by blocking opponent wins.
    3.)  Set up a win on your next turn by choosing so that there is at least
         one available win for each of our opponents moves.
    4.)  Choose such that the oppoent is unable to win on their next turn, and
         that they cannot hit us with rule #3 above.
    5.)  On an empty board, grab a corner.
    6.)  On a non-empty board, grab the center, if possible.
    7.)  On a non-empty board with the center taken, grab a corner.

"""

#generate a tree of moves and outcomes.
def generate_movetree(game):
    return { m : game.apply_move(m) for m in game.get_legal_moves() } 
            
#grab the next "best" gamestate from the current using the rules above
def get_next_gamestate(game, player=None):

    #this is the player that we want to win
    if not player:
        player = game.active_player

    opponent = 'x' if player == 'o' else 'o'

    #if the board is full or game is over:
    if game.winner or game.depth == 9:
        return game

    #if the board is empty, grab 0:
    if game.depth == 0:
        return game.apply_move(0)
        
    #if the board has only one move and the center is available, take it
    #if it is unavailable, take the upper left.
    if game.depth == 1:
        if 4 not in game.get_legal_moves():
            return game.apply_move(0)
        else:
            return game.apply_move(4)

    #if opponent didn't take the opposing corner, take it
    if game.depth == 2 and 8 in game.get_legal_moves():
        return game.apply_move(8)

    #if there is only one possible move, take it
    if len(game.get_legal_moves()) == 1:
        m = game.get_legal_moves()[0]
        return game.apply_move(m)
   
    movetree = generate_movetree(game)

    #check to see if a move creates a win, if so, take it
    wins = [ m for m, gs in movetree.iteritems() if gs.winner == player ]
    if wins:
        return game.apply_move(wins[0])

    #prune any losing moves from the move tree
    #look 1 move ahead
    losing_moves = [ 
        m for m, gs
        in movetree.iteritems() 
        if opponent in [ 
            gs2.winner 
            for m2, gs2 
            in generate_movetree(gs).iteritems() 
        ]
    ]
    for lm in losing_moves:
        del movetree[lm]
    
    #if only one move remains, return it
    if len(movetree) == 1:
        return movetree.values()[0]

    #multi-move look-ahead only matters of turns 6 and below.  In that case,
    #or if no non-losing moves remain, return the first legal move:
    if game.depth > 8 or len(movetree) == 0: 
        return game.apply_move(game.get_legal_moves()[0])

    #look for moves for which all opponents moves result in a loss for them
    #on our next turn
    opponent_movetree = { 
        m : generate_movetree(game.apply_move(m)) 
        for m, gs 
        in movetree.iteritems() 
    }
    for m, mt in opponent_movetree.iteritems():
        ournext = { mx : get_next_gamestate(gx) for mx, gx in mt.iteritems()}
        if len(ournext) == len([ x for x in ournext.values() if x.winner == player ]):
            return game.apply_move(m)

    #look for moves where we'd lose to the same strategy 
    losing_forks = []
    # movetree0 = movetree
    # movetree1 = opponent_movetree
    movetree2 = { 
        m0 : { 
            m1 : generate_movetree(gs1)
            for m1, gs1 
            in generate_movetree(gs0).iteritems()
        }
        for m0, gs0
        in movetree.iteritems()
    }
    for m0, mt0 in movetree2.iteritems():
        for m1, mt1 in mt0.iteritems():
            theirnext =  { mx : get_next_gamestate(gx) for mx, gx in mt1.iteritems() }
            if len(theirnext) == len([ x for x in theirnext.values() if x.winner == opponent ]):
                losing_forks.append(m0) 

    #remove them from the move list
    for lf in list(set(losing_forks)):
        del movetree[lf]

    #default to the first available move of the remaining safe ones
    if len(movetree) > 0:
        return game.apply_move(movetree.keys()[0])

    #if there are no safe moves available, return a random legal move
    return game.apply_move(game.get_legal_moves()[0])
