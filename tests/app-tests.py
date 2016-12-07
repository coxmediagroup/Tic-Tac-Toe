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

    @mock.patch('app.game.calc_ai_move')
    def test_player_turn_added_to_session(self, _calc_ai_move):
        _calc_ai_move.return_value = dict(cell='cell-2:2')
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
                ai_cells=['cell-2:0', 'cell-2:2'],
                player_cells=['cell-1:0'],
            )
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
            expected = game.calc_ai_move(['cell-1:0'], ['cell-0:0'])
            actual = json.loads(resp.data)
            self.assertEqual(actual['mark_cell'], expected['cell'])

    @mock.patch('app.game.calc_ai_move')
    def test_ai_third_move_added_to_session(self, _calc_ai_move):
        _calc_ai_move.return_value = dict(cell='cell-2:0')
        with self.client as c:
            with c.session_transaction() as sess:
                sess['game_state'] = dict(
                    player_turn=True,
                    ai_cells=['cell-0:0'],
                    player_cells=[],
                )
            c.get('/player_turn/cell-0:2/')
            expected = dict(
                player_turn=True,
                ai_cells=['cell-0:0', 'cell-2:0'],
                player_cells=['cell-0:2'],
            )
            actual = session['game_state']
            self.assertEqual(expected, actual)

    @mock.patch('app.game.calc_ai_move')
    def test_win_data(self, _calc_ai_move):
        _calc_ai_move.return_value = dict(
            cell='cell-1:0',
            winning_cells=('cell-0:0', 'cell-1:0', 'cell-2:0'),
            message='I win!',
        )
        with self.client as c:
            with c.session_transaction() as sess:
                sess['game_state'] = dict(
                    player_turn=True,
                    ai_cells=['cell-0:0', 'cell-2:0'],
                    player_cells=['cell-2:2'],
                )
            resp = c.get('/player_turn/cell-0:2/')
            expected_session = dict(
                player_turn=False,
                ai_cells=['cell-0:0', 'cell-2:0', 'cell-1:0'],
                player_cells=['cell-2:2', 'cell-0:2'],
            )
            expected_response = dict(
                mark_cell='cell-1:0',
                winning_cells=['cell-0:0', 'cell-1:0', 'cell-2:0'],
                message='I win!',
            )
            actual_session = session['game_state']
            self.assertEqual(expected_session, actual_session)
            actual_response = json.loads(resp.data)
            self.assertEqual(expected_response, actual_response)

    def test_draw_handled(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['game_state'] = dict(
                    player_turn=True,
                    ai_cells=['cell-0:0', 'cell-2:2', 'cell-0:1'],
                    player_cells=['cell-1:1', 'cell-2:1'],
                )
            resp = c.get('/player_turn/cell-0:2/')
            expected_session = dict(
                player_turn=True,
                ai_cells=['cell-0:0', 'cell-2:2', 'cell-0:1'],
                player_cells=['cell-1:1', 'cell-2:1'],
            )
            expected_response = dict(
                draw_cell='cell-0:2',
                message=("I'm pretty sure you just misclicked. I mean, it's almost as if you want the game "
                         "to end in a draw. I'm going to give you the benefit of the doubt and just assume "
                         "you totally did not intend for this match to be a tie. Lucky you! You get to pick "
                         "again!")
            )
            actual_session = session['game_state']
            self.assertEqual(expected_session, actual_session)
            actual_response = json.loads(resp.data)
            self.assertEqual(expected_response, actual_response)
