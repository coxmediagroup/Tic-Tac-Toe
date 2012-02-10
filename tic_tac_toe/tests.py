#!/usr/bin/env python
from copy import deepcopy
import unittest

import game

class TestCoverage(unittest.TestCase):
    """
    Ensure that all possible games lead to a draw or win for the computer.
    """
    def test_plays(self):
        def _play(ttt):
            for play in ttt.get_open_plays():
                my_ttt = deepcopy(ttt)
                status = my_ttt.play(play.x, play.y)
                if status:
                    print status
                    assert status != game.USER, (
                        '\n%s\nPlays: %s' % (str(my_ttt), my_ttt.history))
                    break
                _play(my_ttt)

        _play(game.TicTacToe(user_starts=True))
        _play(game.TicTacToe(user_starts=False))

if __name__ == '__main__':
    unittest.main()
