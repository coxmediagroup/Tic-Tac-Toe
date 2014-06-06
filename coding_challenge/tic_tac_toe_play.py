from random import choice
from copy import deepcopy
from django.conf import settings
D = settings.D


def get_next_opt_state(state=None, player='x'):
    if not state:
        state = [['e', 'e', 'e'],
                 ['e', 'e', 'e'],
                 ['e', 'e', 'e']]
        choice(state)[choice((0, 1, 2))] = player
        return state

    if has_winner(state) or is_final(state):
        return state

    scores = []
    for next_state in get_next_states(state, player):
        score = get_state_score(next_state,
                                'o' if player == 'x' else 'x',
                                max_player=False)
        scores.append((score, next_state))
    return max(scores, key=lambda t: t[0])[1]


def get_state_score(state, player, max_player):
    if has_winner(state):
        if max_player:
            return -1
        elif not max_player:
            return 1
    elif is_final(state):
        return 0

    scores = []
    for next_state in get_next_states(state, player):
        score = get_state_score(next_state,
                                'o' if player == 'x' else 'x',
                                max_player=not max_player)
        scores.append(score)

    if max_player:
        return max(scores)
    else:
        return min(scores)


def get_next_states(state, player):
    next_states = []
    for i, row in enumerate(state):
        for j, col in enumerate(row):
            if col == 'e':
                next_state = deepcopy(state)
                next_state[i][j] = player
                next_states.append(next_state)
    return next_states


def has_winner(state):
    # This function modifies the input state (uppercase the winning cells)

    for row in state:
        if row[0] == row[1] == row[2] != 'e':
            row[0] = row[1] = row[2] = row[0].upper()
            return True
    for j, col in enumerate(zip(*state)):
        if col[0] == col[1] == col[2] != 'e':
            state[0][j] = state[1][j] = state[2][j] = col[0].upper()
            return True
    if state[0][0] == state[1][1] == state[2][2] != 'e':
        state[0][0] = state[1][1] = state[2][2] = state[0][0].upper()
        return True
    if state[0][2] == state[1][1] == state[2][0] != 'e':
        state[0][2] = state[1][1] = state[2][0] = state[0][2].upper()
        return True


def is_final(state):
    for row in state:
        if 'e' in row:
            return False
    return True
