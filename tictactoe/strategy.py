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

    Uses the Minimax algorithm

    References:
    http://en.wikipedia.org/wiki/Minimax
    http://www.neverstopbuilding.com/minimax

    The basic idea: X will always pick a winning move, O will always pick
    a winning move, and a win for one is a loss for the other.  So, call
    a win for X a positive score and a win for O a negative score, and a
    win today is better than a win next move.  When X plays, pick the
    move that maximizes the score, and when O plays, pick the move that
    minimizes the score
    '''

    _scores = dict()
    _next_moves = dict()

    def next_move(self, board):
        scores = self.score_moves(board)
        my_mark = board.next_mark()
        if my_mark == board.X_NEXT:
            score = max(scores.values())
        else:
            score = min(scores.values())
        return random_choice([k for k, v in scores.items() if v == score])

    def score_moves(self, board):
        state = board.state()
        if state not in MinimaxStrategy._scores:
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
                    nscores = self.score_moves(next_board)
                    if next_board.next_mark() == board.X_NEXT:
                        scores[pos] = max(nscores.values())
                    else:
                        scores[pos] = min(nscores.values())
            MinimaxStrategy._scores[state] = scores
        return MinimaxStrategy._scores[state]
