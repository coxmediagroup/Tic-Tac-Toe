# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from apps.coxtactoe import tictactoe as ttt
from apps.coxtactoe.exceptions import InvalidGameError

import logging as log
log.basicConfig(level=log.INFO)

__docformat__ = 'restructuredtext en'


class GameTests(TestCase):
    def setUp(self):
        self.game = ttt.Game()
        self._ = ttt.Marker('_')
        self.x = ttt.Marker('X')
        self.o = ttt.Marker('O')

    def test_game_initializes(self):
        self.assertIsInstance(self.game, ttt.Game)

    def test_game_save(self):
        self.game.board.place(self.x, 0)
        self.game.save()

    def test_get_game_by_gid(self):
        self.game.board.place(self.x, 0)
        self.game.save()
        saved_game_id = self.game.id
        game = ttt.Game(id=saved_game_id)
        self.assertEquals(self.game.id, game.id)
        self.assertEquals(self.game.board.key, game.board.key)
        self.assertEquals(self.game.board.turn, game.board.turn)

    def _win_game(self, player):
        self.game.board.place(player, 0)
        self.game.board.place(player.opponent, 2)
        self.game.board.place(player, 4)
        self.game.board.place(player.opponent, 3)
        self.game.board.place(player, 8)

    def test_game_over(self):
        self._win_game(self.x)
        self.assertTrue(self.game.over)

    def test_game_winner(self):
        self._win_game(self.x)
        self.assertEquals(self.game.winner, self.x)

    def test_game_reset(self):
        self.game.board.place(self.x, 0)
        self.game.reset()
        self.assertEquals(self.game.board.key, self.game.board.initial_board)

    def test_invalid_game_error_exception(self):
        self.assertRaises(InvalidGameError, ttt.Game, 0)
