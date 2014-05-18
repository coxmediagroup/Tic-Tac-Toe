'''
Defines Tic-Tac-Toe strategies

Each strategy has a 'next_move' method to decide the next move
'''

from random import choice as random_choice

from tictactoe.board import Board


class RandomStrategy(object):
    '''Randomly picks next move'''

    def next_move(self, board):
        return random_choice(board.next_moves())


class MinimaxStrategy(object):
    '''Pick a next move that won't lose

    Uses the Minimax algorithm.  References:
    http://en.wikipedia.org/wiki/Minimax
    http://www.neverstopbuilding.com/minimax

    The basic algorithm:

    Assign a score to each move.  X gets positive scores (5 on turn 5, 3 on
    turn 7, 1 on turn 9) for winning, and O gets negative scores (-4 on turn 6,
    -2 on turn 8) for winning.  A tie gets a 0.  Most moves do no result in a
    win, but require continuing the game.

    The Minimax player tries all the possible moves, looking for wins.  It
    assumes the other player is doing the same.  Determining the best moves
    requires simulating the entire game down to each win or tie, and choosing
    only the paths the player (or the simulated Minimax opponent) would play.
    This results in best possible scores for the next moves in the current
    round.  The Minimax player picks all the moves with the same best score,
    and randomly picks one.

    Two Minimax players will always tie, meaning all starting moves have an
    expected score of 0.  However, if the other player makes a mistake, then
    the Minimax player will quickly go for the win, whether it is this move or
    a few moves down the tree.

    The move tree is cached on calculation.  It takes about 2 seconds to
    calculate on my laptop, and has 4520 items.  A non-expert player may cause
    additional trees to be explored.
    '''

    _best_moves = dict()

    def next_move(self, board):
        '''Pick a random choice from the best moves'''
        score, best_moves = self.best_moves(board)
        return random_choice(best_moves)

    def best_moves(self, board):
        '''Return the moves with an equal chance of winning'''
        state = board.state()
        if state not in MinimaxStrategy._best_moves:
            scores = self.score_moves(board)
            my_mark = board.next_mark()
            if my_mark == board.X_NEXT:
                score = max(scores.values())
            else:
                score = min(scores.values())
            next_moves = [k for k, v in scores.items() if v == score]
            MinimaxStrategy._best_moves[state] = (score, sorted(next_moves))
        score, moves = MinimaxStrategy._best_moves[state]
        return score, moves

    def score_moves(self, board):
        '''Score next moves for a board'''
        scores = {}
        depth = 9 - len(board.next_moves())
        for pos in board.next_moves():
            next_board = Board(board.state())
            next_board.move(pos)
            if next_board.winner() == board.X_WINS:
                scores[pos] = 10 - depth
            elif next_board.winner() == board.O_WINS:
                scores[pos] = -10 + depth
            elif next_board.winner() == board.TIE:
                scores[pos] = 0
            else:
                score, moves = self.best_moves(next_board)
                scores[pos] = score
        return scores
