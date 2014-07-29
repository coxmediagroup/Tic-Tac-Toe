# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from apps.coxtactoe import tictactoe as ttt
from apps.coxtactoe.ai import MinMaxPlayer, X, O

__docformat__ = 'restructuredtext en'


def test_minmax_player_as_x():
    """Has MinMaxPlayer play 1000 games as X. Opponent's play is random.
    """
    ai = MinMaxPlayer(X)
    ai.play()


def test_minmax_player_as_o():
    """Has MinMaxPlayer play 1000 games as O. Opponent's play is random.
    """
    ai = MinMaxPlayer(O)
    ai.player = X  # let X go first
    ai.play()


def test_minmax_player_api():
    """Tests :class:`MinMaxPlayer` interface for playing when state is external
    """
    board = ttt.Board()
    board.place(X, 0)
    ai = MinMaxPlayer(O, board)
    ai_move = ai.get_best_move()
    board.place(O, ai_move)
