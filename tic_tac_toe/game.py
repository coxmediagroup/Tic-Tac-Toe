#!/usr/bin/env python
# -*- coding: latin-1 -*-
import operator
from random import randint

SIZE = 3
USER = 'X'
COMPUTER = 'O'
DRAW = 'DRAW'

class InvalidPlay(Exception):
    pass

class Pos(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.value = None

class TicTacToe(object):
    def __init__(self, user_starts=None):
        self.board = [[Pos(x, y) for y in range(SIZE)] for x in range(SIZE)]
        self.history = []
        self.status = None

        # If the program plays first, then play...
        if user_starts is None:
            user_starts = bool(randint(0, 1))
        if not user_starts:
            play = self.__computer_play()
            self._push_play(COMPUTER, play.x, play.y)

    @classmethod
    def _get_rows(cls, board):
        """Returns the 8 possible winning rows for the specified board."""
        return (
            # horizontal
            [row for row in board]

            # vertical
            + [[row[i] for row in board] for i in range(SIZE)]

            # diagonal
            + [[board[i][i] for i in range(SIZE)]]
            + [[board[i][SIZE-1-i] for i in range(SIZE)]]
        )

    @classmethod
    def _row_winner(cls, row):
        """
        Return the winner of the given row, or `None` if there is no winner.
        """
        if row[0].value and all(
                [row[0].value == row[i].value for i in range(1, SIZE)]):
            return row[0].value
        else:
            return None

    @classmethod
    def _get_winner(cls, rows):
        return reduce(lambda x, y: x or y, map(cls._row_winner, rows))

    @classmethod
    def _get_open_board_plays(cls, board):
        plays = []
        for row in board:
            plays += [x for x in row if not x.value]
        return plays

    def get_open_plays(self):
        return self._get_open_board_plays(self.board)

    def get_status(self):
        winner = self._get_winner(self._get_rows(self.board))
        if winner:
            return winner
        else:
            return DRAW if len(self.history) == SIZE*SIZE else None

    def play(self, x, y):
        """
        Play user at position (x, y).
        Returns the winner (GAME or USER), DRAW, or None if game not over.
        """
        self._push_play(USER, x, y)
        self.status = self.get_status()

        # Computer plays after user, if the board isn't clear.
        if not self.status:
            play = self._get_computer_play()
            self._push_play(COMPUTER, play.x, play.y)
            self.status = self.get_status()

        return self.status

    def _push_play(self, player, x, y):
        if self.status == DRAW:
            raise InvalidPlay, 'The game is already over.  The game is a draw.'
        elif self.status:
            raise InvalidPlay, '`%s` has already won the game.' % self.winner
        elif self.board[x][y].value:
            raise InvalidPlay, '(%s, %s) has already been played.' % (x, y)
        else:
            self.board[x][y].value = player
            self.history.append((player, (x, y)))

    def _pop_play(self):
        last_player, last_play = self.history.pop()
        self.board[last_play[0]][last_play[1]].value = None

    def _get_computer_play(self):
        # Special-case playing the center piece from strategy here:
        # http://en.wikipedia.org/wiki/Tic-tac-toe#Strategy
        if len(self.history) == 1:
            edge_coords = (0, SIZE-1)
            x, y = self.history[0][1]
            if x in edge_coords and y in edge_coords:
                return self.board[SIZE/2][SIZE/2]

        # Otherwise, calculate play with minimax algorithm.
        fitness, play = self._minimax(COMPUTER)
        return play

    def _minimax(self, player):
        """
        Use the minimax algorithm to determine the best play from a
        protection-standpoint.
        """
        winner = self._get_winner(self._get_rows(self.board))
        if winner == COMPUTER:
            return 1, None
        elif winner == USER:
            return -1, None
        else:
            if player == COMPUTER:
                best_fitness, best_play = float('-inf'), None
                op = operator.gt
                next_player = USER
            else:
                best_fitness, best_play = float('inf'), None
                op = operator.lt
                next_player = COMPUTER

            for play in self.get_open_plays():
                self._push_play(player, play.x, play.y)
                fitness, depth_play = self._minimax(next_player)
                self._pop_play()
                if op(fitness, 0):
                    return fitness, play
                elif op(fitness, best_fitness):
                    best_fitness, best_play = fitness, play
            return best_fitness, best_play

    def __str__(self):
        return '\n'.join([' '.join([self.board[x][y].value or '·'
            for x in range(SIZE)]) for y in range(SIZE)])

if __name__ == '__main__':
    t = TicTacToe(user_starts=True)
    t.play(0,0)
    print t
