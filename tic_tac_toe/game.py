#!/usr/bin/env python
# -*- coding: latin-1 -*-
from random import randint

SIZE = 3
USER = 'X'
COMP = 'O'

class InvalidPlay(Exception):
    pass

class Pos(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.value = None

    def __repr__(self):
        #return str(self.value)
        return '(%s, %s)' % (self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class TicTacToe(object):
    def __init__(self, user_starts=None):
        self.board = [[Pos(x, y) for y in range(SIZE)] for x in range(SIZE)]
        self.history = []
        self.winner = None

        # If the program plays first, then play...
        if user_starts is None:
            user_starts = bool(randint(0, 1))
        if not user_starts:
            self._take_turn()

    def get_rows(self):
        """Returns the 8 possible winning rows for the current board."""
        return (
            # horizontal
            [row for row in self.board]

            # vertical
            + [[row[i] for row in self.board] for i in range(SIZE)]

            # diagonal
            + [[self.board[i][i] for i in range(SIZE)]]
            + [[self.board[i][SIZE-1-i] for i in range(SIZE)]]
        )

    def _row_winner(self, row):
        """
        Return the winner of the given row, or `None` if there is no winner.
        """
        if row[0] and all([row[0] == row[i] for i in range(1, SIZE)]):
            return row[0]
        else:
            return None

    def play(self, x, y):
        """
        Play user
        """
        _do_play(USER, x, y)

        self.winner = reduce(
            lambda x, y: x or y,
            map(self._row_winner, self.get_rows())
        )
        return self.winner

    def __str__(self):
        return '\n'.join(
            [' '.join([x.value or '·' for x in row]) for row in self.board]
        )

    def _do_play(self, player, x, y):
        if self.game_over:
            raise InvalidPlay, 'Game is already over.'
        elif self.board.value:
            raise InvalidPlay, '(%s, %s) has already been played.'
        else self.board.value:
            self.board[x][y].value = player
            self.history += (player, (x, y))

        return self.get_game_status()

    def _take_turn(self):
        # Calculate optimal play.  Strategy condensed from:
        # http://en.wikipedia.org/wiki/Tic-tac-toe#Strategy
        # We could use a minimax algorithm here instead, but the rules are
        # straight-forward enough.
        rows = self.get_rows()

        while True:
            # If first play, choose corner.
            if not any()
            self.board[0][0].value = COMP
            break

            # Get rows requiring one more play to win.
            winnable_rows = map(lambda row: )

            # Play winning position, if possible.
            for row in rows:
                pass#if set(row)

        _do_play(COMP, x, y)

if __name__ == '__main__':
    t = TicTacToe()
    print t
