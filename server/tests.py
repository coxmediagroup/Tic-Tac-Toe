import unittest

import endpoints
import mock
import webtest
from google.appengine.ext import ndb
from google.appengine.ext import testbed

import api
import models


NAMESPACE = '1'


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
        game = self.new_game(
            a1='X', a2=None, a3='O',
            b1=None, b2='X', b3=None,
            c1='X', c2='O', c3='O')
        game.put()
        message = {'square': 'b1', 'id': 1}
        response = self.testapp.post_json(
            '/_ah/spi/TicTacToeApi.move', message)
        self.assertIn('outcome', response.json)
        self.assertEqual('won', response.json['outcome'])

    def testMoveTied(self):
        game = self.new_game(
            a1='X', a2=None, a3='O',
            b1='O', b2='O', b3='X',
            c1='X', c2='X', c3='O')
        game.put()
        message = {'square': 'a2', 'id': 1}
        response = self.testapp.post_json(
            '/_ah/spi/TicTacToeApi.move', message)
        self.assertIn('outcome', response.json)
        self.assertEqual('tied', response.json['outcome'])

    def testMoveLost(self):
        game = self.new_game(
            a1='O', a2='X', a3='X',
            b1=None, b2='O', b3=None,
            c1='O', c2='X', c3=None)
        game.put()
        message = {'square': 'c3', 'id': 1}
        response = self.testapp.post_json(
            '/_ah/spi/TicTacToeApi.move', message)
        self.assertIn('outcome', response.json)
        self.assertEqual('lost', response.json['outcome'])

    def testReplay(self):
        game = self.new_game(
            a1='X', a2='X', a3='O',
            b1='O', b2='O', b3='X',
            c1='X', c2='X', c3='O',
            outcome='tied')
        game.put()
        message = {'id': 1}
        response = self.testapp.post_json(
            '/_ah/spi/TicTacToeApi.replay', message)
        self.assertDictEqual({'id': '1'}, response.json)


if __name__ == '__main__':
    unittest.main()
