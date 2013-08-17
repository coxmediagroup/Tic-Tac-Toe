"""Tests for the *cough cough* AI of the
tic-tac-toe game.

Nick Loadholtes <nick@ironboundsoftware.com>
"""
from nose.tools import assert_equal, assert_true

from ttt.ai import randomPlayer


def test_randomPlayer_fills_in_at_least_one():
    board = [None for x in range(0, 9)]
    randomPlayer(board)
    assert_true('X' in board)
