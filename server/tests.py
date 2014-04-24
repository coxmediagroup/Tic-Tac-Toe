import re
import unittest

import endpoints
import mock
import webtest
from google.appengine.ext import testbed

import api
import models


NAMESPACE = '1'


def create_game_from_ascii(ascii):
    pattern = r'(?<=\| )(.)(?= \|)'
    chars = [None if c.isspace() else c for c in re.findall(pattern, ascii)]
    assert len(chars) == 9, 'Expected 9 chars, got %s' % len(chars)
    props = [c + i for c in 'abc' for i in '123']
    kw = dict(zip(props, chars))
    return models.Game(id=1, namespace=NAMESPACE, **kw)


class ApiTest(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.setup_env(current_version_id='1.0')
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

        app = endpoints.api_server([api.TicTacToeApi], restricted=False)
        self.testapp = webtest.TestApp(app)

        mock_user = mock.Mock(**{'user_id.return_value': NAMESPACE})
        patcher = mock.patch.object(
            endpoints, 'get_current_user', return_value=mock_user)
        patcher.start()
        self.addCleanup(patcher.stop)

    def tearDown(self):
        self.testbed.deactivate()

    def new_game(self, **kw):
        return models.Game(id=1, namespace=NAMESPACE, **kw)

    def testStart(self):
        message = {}
        response = self.testapp.post_json(
            '/_ah/spi/TicTacToeApi.start', message)
        self.assertDictEqual({'id': '1'}, response.json)
        self.assertEqual(1, models.Game.query().count())

    def testMoveWon(self):
        game = create_game_from_ascii("""
            +---+---+---+
            | X |   | O |
            +---+---+---+
            |   | X |   |
            +---+---+---+
            | X | O | O |
            +---+---+---+
            """)
        game.put()
        message = {'square': 'b1', 'id': 1}
        response = self.testapp.post_json(
            '/_ah/spi/TicTacToeApi.move', message)
        self.assertIn('outcome', response.json)
        self.assertEqual('won', response.json['outcome'])

    def testMoveTied(self):
        game = create_game_from_ascii("""
            +---+---+---+
            | X |   | O |
            +---+---+---+
            | O | O | X |
            +---+---+---+
            | X | O | O |
            +---+---+---+
            """)
        game.put()
        message = {'square': 'a2', 'id': 1}
        response = self.testapp.post_json(
            '/_ah/spi/TicTacToeApi.move', message)
        self.assertIn('outcome', response.json)
        self.assertEqual('tied', response.json['outcome'])

    def testMoveLost(self):
        game = create_game_from_ascii("""
            +---+---+---+
            | O | X | X |
            +---+---+---+
            |   | O |   |
            +---+---+---+
            | O | X |   |
            +---+---+---+
            """)
        game.put()
        message = {'square': 'c3', 'id': 1}
        response = self.testapp.post_json(
            '/_ah/spi/TicTacToeApi.move', message)
        self.assertIn('outcome', response.json)
        self.assertEqual('lost', response.json['outcome'])

    def testReplay(self):
        game = create_game_from_ascii("""
            +---+---+---+
            | X | X | O |
            +---+---+---+
            | O | O | X |
            +---+---+---+
            | X | X | O |
            +---+---+---+
            """)
        game.outcome = 'tied'
        game.put()
        message = {'id': 1}
        response = self.testapp.post_json(
            '/_ah/spi/TicTacToeApi.replay', message)
        self.assertDictEqual({'id': '1'}, response.json)


class GameTest(unittest.TestCase):

     def testValues(self):
        game = create_game_from_ascii("""
            +---+---+---+
            | O | X | X |
            +---+---+---+
            |   | O |   |
            +---+---+---+
            | O | X |   |
            +---+---+---+
            """)
        self.assertListEqual(
            ['O', 'X', 'X', None, 'O', None, 'O', 'X', None],
            game.values())

     def testReset(self):
        game = create_game_from_ascii("""
            +---+---+---+
            | X | X | O |
            +---+---+---+
            | O | O | X |
            +---+---+---+
            | X | X | O |
            +---+---+---+
            """)
        game.outcome = 'tied'
        game.reset()
        self.assertListEqual([None] * 9, game.values())

     def testIsEmptySquare(self):
        game = create_game_from_ascii("""
            +---+---+---+
            | O | X | X |
            +---+---+---+
            |   | O |   |
            +---+---+---+
            | O | X |   |
            +---+---+---+
            """)
        self.assertFalse(game.is_empty_square('a1'))
        self.assertFalse(game.is_empty_square('a2'))
        self.assertFalse(game.is_empty_square('a3'))
        self.assertTrue(game.is_empty_square('b1'))
        self.assertFalse(game.is_empty_square('b2'))
        self.assertTrue(game.is_empty_square('b3'))
        self.assertFalse(game.is_empty_square('c1'))
        self.assertFalse(game.is_empty_square('c2'))
        self.assertTrue(game.is_empty_square('c3'))

     def testHasOppositeCorners(self):
        game = create_game_from_ascii("""
            +---+---+---+
            | X |   |   |
            +---+---+---+
            |   | O |   |
            +---+---+---+
            |   |   | X |
            +---+---+---+
            """)
        self.assertTrue(game.has_opposite_corners())
        game = create_game_from_ascii("""
            +---+---+---+
            | X |   |   |
            +---+---+---+
            |   | O |   |
            +---+---+---+
            |   | X |   |
            +---+---+---+
            """)
        self.assertFalse(game.has_opposite_corners())

     def testGetWinningSquare(self):
        game = create_game_from_ascii("""
            +---+---+---+
            | O | X | X |
            +---+---+---+
            |   | O |   |
            +---+---+---+
            | O | X | X |
            +---+---+---+
            """)
        self.assertEqual('b1', game.get_winning_square())

     def testGetBlockingSquare(self):
        game = create_game_from_ascii("""
            +---+---+---+
            | O | X | X |
            +---+---+---+
            | X | O |   |
            +---+---+---+
            | O |   | X |
            +---+---+---+
            """)
        self.assertEqual('b3', game.get_blocking_square())

     def testGetCenterSquare(self):
        game = create_game_from_ascii("""
            +---+---+---+
            |   |   |   |
            +---+---+---+
            |   |   |   |
            +---+---+---+
            |   |   |   |
            +---+---+---+
            """)
        self.assertEqual('b2', game.get_center_square())
        game = create_game_from_ascii("""
            +---+---+---+
            |   |   |   |
            +---+---+---+
            |   | X |   |
            +---+---+---+
            |   |   |   |
            +---+---+---+
            """)
        self.assertIsNone(game.get_center_square())

     def testGetMostDisruptiveSquare(self):
        game = create_game_from_ascii("""
            +---+---+---+
            | X |   |   |
            +---+---+---+
            |   | O |   |
            +---+---+---+
            |   | X |   |
            +---+---+---+
            """)
        self.assertEqual('c1', game.get_most_disruptive_square())

     def testGetRandomSquare(self):
        game = create_game_from_ascii("""
            +---+---+---+
            | X |   |   |
            +---+---+---+
            |   |   |   |
            +---+---+---+
            |   |   |   |
            +---+---+---+
            """)
        squares = ['a1', 'c1', 'c3', 'a3']
        with mock.patch('random.shuffle', return_value=squares):
            self.assertEqual('c1', game.get_random_square(squares))

     def testGetBestSquare(self):
        game = create_game_from_ascii("""
            +---+---+---+
            |   |   |   |
            +---+---+---+
            |   | X |   |
            +---+---+---+
            |   |   |   |
            +---+---+---+
            """)
        with mock.patch.object(game, 'get_random_square', return_value='a3'):
            self.assertEqual('a3', game.get_best_square())

     def testIsWon(self):
        game = create_game_from_ascii("""
            +---+---+---+
            | O | X | X |
            +---+---+---+
            | O | O |   |
            +---+---+---+
            | O | X | X |
            +---+---+---+
            """)
        self.assertFalse(game.is_won('X'))
        self.assertTrue(game.is_won('O'))

     def testIsTied(self):
        game = create_game_from_ascii("""
            +---+---+---+
            | X | X | O |
            +---+---+---+
            | O | O | X |
            +---+---+---+
            | X | X | O |
            +---+---+---+
            """)
        self.assertTrue(game.is_tied())
        game.a1 = None
        self.assertFalse(game.is_tied())


if __name__ == '__main__':
    unittest.main()
