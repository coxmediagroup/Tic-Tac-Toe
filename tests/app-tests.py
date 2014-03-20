import unittest
import json

from flask import session
import mock

import app


class TestComputerFirst(unittest.TestCase):

    def setUp(self):
        self.app = app.app
        self.client = app.app.test_client()

    def test_ai_move_one(self):
        resp = self.client.get('/ai_first/')
        actual = json.loads(resp.data)
        self.assertIn(actual['mark_cell'], ['c1', 'c3', 'c7', 'c9'])

    @mock.patch('app.game.ai_move_one')
    def test_session_move_one(self, _ai_move_one):
        _ai_move_one.return_value = 'c1'
        expected = dict(
            ai_cells=['c1'],
            player_cells=[],
        )
        with self.client as c:
            c.get('/ai_first/')
            actual = session['game_state']
            self.assertEqual(expected, actual)
