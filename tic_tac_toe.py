from random import choice


def get_next_state(state=None, player='x'):
    if not state:
        state = [['', '', ''],
                 ['', '', ''],
                 ['', '', '']]
        choice(state)[choice((0, 1, 2))] = player
        return state
    return get_next_opt_state(state, player, max_player=True)[1]


def get_next_opt_state(state, player, max_player):
    if has_winner(state):
        if max_player:
            return (-1,)
        elif not max_player:
            return (1,)
    elif is_final(state):
        return (0,)

    scores = []
    for next_state in get_next_states(state, player):
        score, _ = get_next_opt_state(next_state,
                                      'o' if player == 'x' else 'x',
                                      max_player=not max_player)
        scores.append((score, next_state))
    if max_player:
        return max(scores, key=lambda t: t[0])
    else:
        return min(scores, key=lambda t: t[0])


def get_next_states(state, player):
    next_states = []
    for i, row in enumerate(state):
        for j, col in enumerate(row):
            if not col:
                next_state = list(state)
                next_state[i] = list(state[i])
                next_state[i][j] = player
                next_states.append(next_state)
    return next_states


def has_winner(state):
    for row in state:
        if row[0] == row[1] == row[2] != '':
            return True
    for col in zip(*state):
        if col[0] == col[1] == col[2] != '':
            return True
    if state[0][0] == state[1][1] == state[2][2] != '':
        return True
    if state[0][2] == state[1][1] == state[2][0] != '':
        return True


def is_final(state):
    for row in state:
        if '' in row:
            return False
    return True
