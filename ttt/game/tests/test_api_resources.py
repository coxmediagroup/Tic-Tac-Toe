
from datetime import datetime
from tastypie.test import ResourceTestCase

from game.models import Game
from game.api.resources import GameResource


class GameResourceTest(ResourceTestCase):
    def setUp(self):
        super(GameResourceTest, self).setUp()

        self.game = Game.create_new(True)

        self.game_url = u'/api/v1/game/{0}/'.format(self.game.id)

    def test_get_list_json(self):
        resp = self.api_client.get('/api/v1/game/', format='json')

        self.assertValidJSONResponse(resp)

        json = self.deserialize(resp)

        self.assertEqual(len(json['objects']), 1)
        self.assertEqual(json['objects'][0], {
            u'id': self.game.id,
            u'resource_uri': self.game_url,
            u'started': self.game.started.isoformat()[:-6],
            u'ended': None,
            u'status': u'In Progress',
            u'user_token': 1,
        })

    def test_get_detail_json(self):
        resp = self.api_client.get('/api/v1/game/1/', format='json')

        self.assertValidJSONResponse(resp)

        json = self.deserialize(resp)
        self.assertEqual(json, {
            u'id': self.game.id,
            u'resource_uri': self.game_url,
            u'started': self.game.started.isoformat()[:-6],
            u'ended': None,
            u'status': u'In Progress',
            u'user_token': 1,
            u'board': {
                u'upper_left': 0,
                u'upper_center': 0,
                u'upper_right': 0,
                u'center_left': 0,
                u'center': 0,
                u'center_right': 0,
                u'lower_left': 0,
                u'lower_center': 0,
                u'lower_right': 0,
                u'last_played': self.game._board.last_played.isoformat()[:-6],
                u'resource_uri': '/api/v1/board/{0}/'.format(
                    self.game._board.id),
            }
        })

    def test_post_list(self):
        self.assertEqual(Game.objects.count(), 1)
        self.assertHttpCreated(self.api_client.post('/api/v1/game/', format='json', data={}))
        self.assertEqual(Game.objects.count(), 2)

    def test_detail_patch(self):
        self.assertEqual(self.game.user_token, 1)
        self.assertHttpAccepted(
            self.api_client.patch(
                self.game_url, 
                format='json', 
                data={'center':1}, 
                ))
        self.assertEqual(Game.objects.get(id=1)[1][1], 1)

    def test_detail_post(self):
        self.assertHttpMethodNotAllowed(
            self.api_client.post(
                self.game_url, 
                format='json', 
                data={'center':1}, 
                ))

    def test_detail_put(self):
        self.assertHttpMethodNotAllowed(
            self.api_client.put(
                self.game_url, 
                format='json', 
                data={'center':1}, 
                ))

    def test_detail_delete(self):
        self.assertHttpMethodNotAllowed(
            self.api_client.delete(
                self.game_url, 
                format='json', 
                ))
