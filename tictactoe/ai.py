

__all__ = ['get_move_position']


def get_move_position(board, player):
    """Retrieve the optimal move position for the given board and player.

    """
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


def minimax(board, player, max_player=None):
    """Brute-force minimax implementation."""
    if not max_player:
        max_player = player
    if board.is_game_over():
        return compute_score(board, max_player)
    opponent = board.get_opponent(player)
    scores = [minimax(board.get_board_for_move(opponent, move),
                      opponent,
                      max_player=max_player)
              for move in board.valid_moves]
    if player == max_player:
        return max(scores)
    else:
        return min(scores)
