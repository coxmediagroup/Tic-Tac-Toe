#!/usr/bin/env python
# -*- coding: latin-1 -*-
from copy import deepcopy
import itertools
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
            fitness, play = self._minimax(COMPUTER, self.board)
            self._do_play(COMPUTER, play.x, play.y)

    @classmethod
    def get_rows(cls, board):
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
        winner = self._get_winner(self.get_rows(self.board))
        if winner:
            return winner
        else:
            return DRAW if len(self.history) == SIZE*SIZE else None

    def play(self, x, y):
        """
        Play user at position (x, y).
        Returns the winner (GAME or USER), DRAW, or None if game not over.
        """
        self._do_play(USER, x, y)
        self.status = self.get_status()

        # Computer plays after user, if the board isn't clear.
        if not self.status:
            fitness, play = self._minimax(COMPUTER, self.board)
            self._do_play(COMPUTER, play.x, play.y)
            self.status = self.get_status()

        return self.status

    def _do_play(self, player, x, y):
        if self.status == DRAW:
            raise InvalidPlay, 'The game is already over.  The game is a draw.'
        elif self.status:
            raise InvalidPlay, '`%s` has already won the game.' % self.winner
        elif self.board[x][y].value:
            raise InvalidPlay, '(%s, %s) has already been played.' % (x, y)
        else:
            #print 'Playing %s at (%s, %s)' % (player, x, y)
            self.board[x][y].value = player
            self.history.append((player, (x, y)))
        #print self

    def _minimax(self, player, board):
        """
        Use the minimax algorithm to determine the best play from a
        protection-standpoint.
        """
        winner = self._get_winner(self.get_rows(board))
        if winner == COMPUTER:
            return 1
        elif winner == USER:
            return -1
        else:
            if player == COMPUTER:
                max_fitness, max_play = float('-inf'), None
                for play in self._get_open_board_plays(board):
                    my_board = deepcopy(board)
                    my_board[play.x][play.y].value = COMPUTER
                    fitness = self._minimax(USER, my_board)
                    if fitness > max_fitness:
                        max_fitness, max_play = fitness, play
                    # skip out early to avoid extra passes
                    if max_fitness > 0:
                        break
                return max_fitness, max_play
            else:
                min_fitness, min_play = float('inf'), None
                for play in self._get_open_board_plays(board):
                    my_board = deepcopy(board)
                    my_board[play.x][play.y].value = USER
                    fitness = self._minimax(COMPUTER, my_board)
                    if fitness < min_fitness:
                        min_fitness, min_play = fitness, play
                    # skip out early to avoid extra passes
                    if min_fitness < 0:
                        break
                return min_fitness, min_play

    def __str__(self):
        return '\n'.join([' '.join([self.board[x][y].value or '·'
            for x in range(SIZE)]) for y in range(SIZE)])

if __name__ == '__main__':
    t = TicTacToe(user_starts=False)
    t.play(1,1)
    t.play(0,2)
    t.play(2,2)
    t.play(2,1)
