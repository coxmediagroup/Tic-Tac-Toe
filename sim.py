import random
import sys
import xsos

def random_move(grid_inst, mark):
    """
    Returns a random move pair in the format (row,col) for the given mark using
    the move positions provided by the given Grid instance.
    """
    g = grid_inst
    moves = g._get_moves()
    random.shuffle(moves)
    for r,c in moves:
        if not g.grid[r][c]:
            return (r,c)

def simulate_game(grid_inst):
    """
    Simulates a game using the given Grid instance.
    
    Returns a pair containing the winning mark or Grid.cat and the computer
    player mark. e.g. ('Cat', 'X') or ('X', 'X')
    
    >>> g = xsos.Grid()
    >>> result = simulate_game(g)
    >>> result[0] == g.cat or result[0] == result[1]
    True
    """
    g = grid_inst
    g.reset()
    over, winner = g.game_over()
    # randomize which mark will be random
    cmp_mark = random.choice((1,2))
    while not over:
        # x will always go first
        if cmp_mark == 1:
            g.move(1)
            over, winner = g.game_over()
            if over: break
            r,c = random_move(g,2)
            g.grid[r][c] = 2
            over, winner = g.game_over()
        else:
            r,c = random_move(g,1)
            g.grid[r][c] = 1
            over, winner = g.game_over()
            if over: break
            g.move(2)
            over, winner = g.game_over()
    return winner, g.marks[cmp_mark]

if __name__ == '__main__':
    if len(sys.argv) > 1:
        SIM_LIMIT = int(sys.argv[1])
    else:
        print("Please provide the number of games to simulate.")
        print("For example, to simulate 1000 games:\npython sim.py 1000")
        sys.exit(1)
    #SIM_LIMIT = 10000
    results = []
    g = xsos.Grid()
    while len(results) < SIM_LIMIT:
        results.append(simulate_game(g))
    cmp_win_count = len([x for x in results if x[0] == x[1]])
    rnd_win_count = len([x for x in results if x[0] != x[1] and x[0] != g.cat])
    cat_win_count = len([x for x in results if x[0] == g.cat])
    game_count = len(results)
    print("%d games were simulated." % game_count)
    print("Computer won %d games, the cat won %d, and the random player won %d."%(cmp_win_count, cat_win_count, rnd_win_count))
    sys.exit(0)