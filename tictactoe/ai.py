import random


__all__ = ['get_move_position']


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
    move_scores = [
        (move, minimax(board.get_board_for_move(player, move), player))
         for move in board.valid_moves]
    move_scores.sort(key=lambda(move, score): score)
    return move_scores


def compute_score(board, player):
    winner = board.get_winner()
    if winner == player:
        return 1
    elif not winner:
        return 0
    return -1


def minimax(board, player, min_player=None):
    """Brute-force minimax implementation."""
    if not min_player:
        min_player = player
    if board.is_game_over():
        return compute_score(board, min_player)
    opponent = board.get_opponent(player)
    scores = []
    for move in board.valid_moves:
        move_board = board.get_board_for_move(opponent, move)
        score = minimax(move_board, opponent, min_player=min_player)
        scores.append(score)
    is_min_turn = (player == min_player)
    if is_min_turn:
        return min(scores)
    else:
        return max(scores)
