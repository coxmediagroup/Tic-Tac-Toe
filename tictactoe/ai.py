import random


__all__ = ['get_move_position']


infinity = 1.0e400


def get_move_position(board, player):
    """Retrieve the optimal move position for the given board and player.

    """
    is_empty_board = len(board.valid_moves) == 9
    # A corner is always the optimal move position for an empty board
    if is_empty_board:
        return random.choice([0, 2, 6, 8])
    move_scores = get_move_scores(board, player)
    return move_scores[-1][0]


def get_move_scores(board, player):
    move_scores = []
    for move in board.valid_moves:
        move_board = board.get_board_for_move(player, move)
        score = minimax(move_board, player, -infinity, infinity)
        move_scores.append((move, score))
    # Re-order scores to provide a semblance of non-deterministic behaviour
    random.shuffle(move_scores)
    move_scores.sort(key=lambda(move, score): score)
    return move_scores


def compute_score(board, player):
    winner = board.get_winner()
    if winner == player:
        return 1
    elif not winner:
        return 0
    return -1


def minimax(board, player, alpha, beta, max_player=None):
    """Brute-force minimax with alpha-beta pruning.

    See: http://en.wikipedia.org/wiki/Alpha-beta_pruning

    """
    if not max_player:
        max_player = player
    if board.is_game_over():
        return compute_score(board, max_player)
    opponent = board.get_opponent(player)
    move_boards = (
        board.get_board_for_move(opponent, x) for x in board.valid_moves
        )
    is_max_turn = (opponent == max_player)
    if is_max_turn:
        for move_board in move_boards:
            score = minimax(move_board, opponent, alpha,
                            beta, max_player=max_player)
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return alpha
    else:
        for move_board in move_boards:
            score = minimax(move_board, opponent, alpha,
                            beta, max_player=max_player)
            beta = min(beta, score)
            if beta <= alpha:
                break
        return beta
