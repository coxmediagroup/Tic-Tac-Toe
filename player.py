# players logic

import random
from minimax import minimax
from minimax import infinity


def human(game, state):
    game.display(state)
    row,col = str(raw_input('Your move, eg (1,2) or 1,3? ')).strip().split(',')
    return (int(row),int(col))


def computer(game, state):
    game.display(state)
    value = infinity
    best_moves = []
    for move, state in game.successors(state):
        v = minimax(game, state)
        if v < value:
            value = v
            best_moves = [(v, move)]
        elif v == value:
            best_moves.append((v, move))
    return random.choice(best_moves)[1]
