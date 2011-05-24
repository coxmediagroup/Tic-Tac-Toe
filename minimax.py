# minimax score evaluation utilities for computer player


infinity = 1e400


def minimax(game, state, alpha=-infinity, beta=infinity):
    """minimax algorithm with alpha beta pruning"""

    if game.terminal_state(state):
        return game.utility(state)

    successors = game.successors(state)
    if game.player_MAX(state):
        for _, state in successors:
            alpha = max(alpha, minimax(game, state, alpha, beta))
            if beta <= alpha:
                break # beta cutoff
        return alpha
    elif game.player_MIN(state):
        for _, state in successors:
            beta = min(beta, minimax(game, state, alpha, beta))
            if beta <= alpha:
                break # alpha cutoff
        return beta
