from copy import deepcopy
from random import choice


def convert_repr(play_func):
    def wrapped_play_func(current_state, player):
        if current_state:
            current_state = from_str(current_state)
        next_state = play_func(current_state, player)
        return to_str(next_state)
    return wrapped_play_func


def get_next_opt_state(state=None, player='x'):
    if not state:
        state = [['e', 'e', 'e'],
                 ['e', 'e', 'e'],
                 ['e', 'e', 'e']]
        choice(state)[choice((0, 1, 2))] = player
        return state

    best_score = -2
    best_move = state
    for next_state in get_next_states(state, player):
        score = get_state_score(next_state,
                                'o' if player == 'x' else 'x',
                                max_player=False,
                                best_possible_score=1)
        if score > best_score:
            best_score = score
            best_move = next_state

    final_state = get_winning_state(best_move) or is_final(best_move)
    if final_state:
        print "### FINAL STATE"
        return final_state

    return best_move


def get_state_score(state, player, max_player, best_possible_score):
    if get_winning_state(state):
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
        for j, col_val in enumerate(row):
            if col_val == 'e':
                next_state = list(state)
                next_state[i] = list(row)
                next_state[i][j] = player
                next_states.append(next_state)
    return next_states


def get_winning_state(state):
    def upcase_straight_line(player, *indices):
        winning_state = deepcopy(state)
        player = player.upper()
        for r, c in indices:
            winning_state[r][c] = player
        return winning_state

    for i, row in enumerate(state):
        if row[0] == row[1] == row[2] != 'e':
            return upcase_straight_line(row[0], (i, 0), (i, 1), (i, 2))

    for j, col in enumerate(zip(*state)):
        if col[0] == col[1] == col[2] != 'e':
            return upcase_straight_line(col[0], (0, j), (1, j), (2, j))

    if state[0][0] == state[1][1] == state[2][2] != 'e':
        return upcase_straight_line(state[0][0], (0, 0), (1, 1), (2, 2))

    if state[0][2] == state[1][1] == state[2][0] != 'e':
        return upcase_straight_line(state[0][2], (0, 2), (1, 1), (2, 0))


def is_final(state):
    for row in state:
        if 'e' in row:
            return False
    return state

from_str = lambda state: [list(state[i:i+3]) for i in (0, 3, 6)]
to_str = lambda state: ''.join([''.join(r) for r in state])
