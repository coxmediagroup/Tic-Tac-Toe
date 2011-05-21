

__all__ = ['get_move']


def get_move(player, board):
    move_scores = get_move_scores(player, board)
    return move_scores[-1][0]


def get_move_scores(player, board):
    move_scores = [
        (move, minimax(player, board.get_board_for_move(player, move)))
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


def minimax(player, board, max_player=None):
    """Brute-force minimax implementation."""
    if not max_player:
        max_player = player
    if board.is_game_over():
        return compute_score(board, max_player)
    opponent = board.get_opponent(player)
    scores = [minimax(opponent,
                      board.get_board_for_move(opponent, move),
                      max_player=max_player)
              for move in board.valid_moves]
    if player == max_player:
        return max(scores)
    else:
        return min(scores)
