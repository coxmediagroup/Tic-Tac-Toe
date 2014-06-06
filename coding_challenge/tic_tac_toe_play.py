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

    best_score = -2
    best_move = None
    for next_state in get_next_states(state, player):
        score = get_state_score(next_state,
                                'o' if player == 'x' else 'x',
                                max_player=False,
                                best_possible_score=1)
        if score > best_score:
            best_score = score
            best_move = next_state

    return best_move


def get_state_score(state, player, max_player, best_possible_score):
    if has_winner(state):
        if max_player:
            return -best_possible_score
        elif not max_player:
            return best_possible_score
    elif is_final(state):
        return 0

    best_max_score = -best_possible_score - 1
    best_min_score = best_possible_score + 1
    for next_state in get_next_states(state, player):
        score = get_state_score(next_state,
                                'o' if player == 'x' else 'x',
                                max_player=not max_player,
                                best_possible_score=best_possible_score)
        if max_player:
            if score > best_max_score:
                best_max_score = score
                if best_max_score == best_possible_score:
                    return best_max_score
        else:
            if score < best_min_score:
                best_min_score = score
                if best_min_score == -best_possible_score:
                    return best_min_score
    if max_player:
        return best_max_score
    else:
        return best_min_score


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
