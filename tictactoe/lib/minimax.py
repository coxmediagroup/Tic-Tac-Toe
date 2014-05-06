def winning_state(state):
    """
    Takes a state in the form: list('XX-O--OXX')

    Returns Boolean, character, and a tuple:
      - True if the state is a winning state.
      - The marker of the winning player.
      - The winning combination.

    The board spaces are represented as integers,
    corresponding to the following:

      0 1 2
      3 4 5
      6 7 8
    """
    win_states = (
            (0,3,6),
            (1,4,7),
            (2,5,8),
            (0,1,2),
            (3,4,5),
            (6,7,8),
            (0,4,8),
            (2,4,6),
        )

    is_winning_state = False
    for s in win_states:
        if all(state[s[0]]==state[s[1]],state[s[1]]==state[s[2]],state[s[0]]!='-'):
            return True, state[s[0]], s
    return False, '-', ()

def next_move(state,player):
    """
    Takes a state in the form: list('XX-O--OXX')

    Returns two integers:
      - The first integer is one of -1, 0, or 1.
        This represents the score of the most 
        favorable branch.
      - The second integer is the next move
        required to enter the max branch.

    The board spaces are represented as integers,
    corresponding to the following:

      0 1 2
      3 4 5
      6 7 8
    """
    if player=='X':
        next_player = 'O'
    else:
        next_player = 'O'

    if len(set(state)) == 1:
        return 0,4

    win_state, win_player, win_pos = winning_state(state)
    if win_state:
        if win_player == 'X':
            return -1,-1
        else:
            return 1,-1

    possible_moves = []
    free_spaces = [ i for i in xrange(0,len(state)) if state[i] == '-' ]
    if len(free_spaces) == 0:
        return 0,-1

    for i in free_spaces:
        state[i] = player
        score,move = next_move(state,next_player)
        possible_moves.append( (score,move) ) 
        state[i] = '-'

    if player == 'X':
        return = max(possible_moves)
    else :
        return min(possible_moves)
