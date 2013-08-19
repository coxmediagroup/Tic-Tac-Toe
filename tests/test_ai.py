"""Tests for the *cough cough* AI of the
tic-tac-toe game.

Nick Loadholtes <nick@ironboundsoftware.com>
"""
from nose.tools import assert_equal, assert_true

from ttt.ai import randomPlayer, _scoreBoard, winningPlayer


def test_randomPlayer_fills_in_at_least_one():
    board = [None for x in range(0, 9)]
    randomPlayer(board)
    assert_true('X' in board)


def test_scoreBoard_start():
    b = [None for x in range(0, 9)]
    output = _scoreBoard(b)
    assert_equal([3, 1, 2, 1, 1, 1, 2, 1, 2], output)


def test_scoreBoard_third_move():
    b = ['X', None, 'O', None, None, None, None, None, None]
    output = _scoreBoard(b)
    assert_equal([0, 1, 0, 1, 1, 1, 2, 1, 2], output)


def test_winningPlayer_first_move():
    b = [None for x in range(0, 9)]
    # import ipdb; ipdb.set_trace()
    winningPlayer(b)
    # print(wp_SCORES)
    assert_equal(['X', None, None, None, None, None, None, None, None], b)
