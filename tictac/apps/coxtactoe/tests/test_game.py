# -*- coding: utf-8 -*-
__docformat__ = 'restructuredtext en'
import unittest

from coxtactoe import tictactoe as ttt
from coxtactoe import const as C

import logging as log
log.basicConfig(level=log.INFO)


class GameTests(unittest.TestCase):
    def setUp(self):
        self.game = ttt.Game()

    def test_game_initializes(self):
        log.debug(self.game.id)
        repr(self.game)

