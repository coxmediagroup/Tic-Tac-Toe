import unittest
import json

from flask import session
import mock

import app
import game


class TestComputerFirst(unittest.TestCase):

    def setUp(self):
        self.app = app.app
        self.client = app.app.test_client()

    def test_ai_move_one(self):
        resp = self.client.get('/ai_first/')
        actual = json.loads(resp.data)
        expected = ['cell-0:0', 'cell-0:2', 'cell-1:1', 'cell-2:0', 'cell-2:2']
        self.assertIn(actual['mark_cell'], expected)

    @mock.patch('app.game.ai_move_one')
    def test_session_move_one(self, _ai_move_one):
        _ai_move_one.return_value = 'cell-0:0'
        expected = dict(
            ai_cells=['cell-0:0'],
            player_cells=[],
            player_turn=True,
        )
        with self.client as c:
            c.get('/ai_first/')
            actual = session['game_state']
            self.assertEqual(expected, actual)

    def test_player_turn_false(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['game_state'] = dict(
                    ai_cells=[],
                    player_cells=[],
                    player_turn=False,
                )
            resp = c.get('/player_turn/cell-0:0/')
            self.assertEqual(409, resp.status_code)

    def test_player_turn_cell_disabled(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['game_state'] = dict(
                    player_turn=True,
                    ai_cells=['cell-0:0'],
                    player_cells=['cell-0:2'],
                )
            resp = c.get('/player_turn/cell-0:0/')
            self.assertEqual(410, resp.status_code)

    def test_player_turn_added_to_session(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['game_state'] = dict(
                    player_turn=True,
                    ai_cells=['cell-2:0'],
                    player_cells=[],
                )
            resp = c.get('/player_turn/cell-1:0/')
            self.assertEqual(200, resp.status_code)
            expected = dict(
                player_turn=True,
                ai_cells=['cell-2:0'],
                player_cells=['cell-1:0'],
            )
            expected = json.loads(json.dumps(expected))  # lazy man's unicode keys
            self.assertEqual(expected, session['game_state'])

    def test_player_turn_invalid_cell(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['game_state'] = dict(
                    player_turn=True,
                    ai_cells=[],
                    player_cells=[],
                )
            resp = c.get('/player_turn/bob/')
            self.assertEqual(404, resp.status_code)

    def test_ai_third_move_returned(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['game_state'] = dict(
                    player_turn=True,
                    ai_cells=['cell-0:0'],
                    player_cells=[],
                )
            resp = c.get('/player_turn/cell-1:0/')
            self.assertEqual(200, resp.status_code)
            expected_cell = game.calc_ai_move(['cell-1:0'], ['cell-0:0'])
            actual = json.loads(resp.data)
            self.assertEqual(actual['mark_cell'], expected_cell)
