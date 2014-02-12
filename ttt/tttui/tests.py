from django.test import TestCase
import json

from game.models import *
from game.player import Computer


class ViewTest(TestCase):
    def setUp(self):
        Game.create_new()
        Game.create_new()
        Game.create_new()

        assert Game.objects.count() == 3

        self.max_id = 3

    def test_get_all_root(self):
        response = self.client.get('')

        assert response.status_code == 200
        assert len(response.context['games']) == 3
        assert response.context['games'][0].id == 1
        assert response.context['games'][1].id == 2
        assert response.context['games'][2].id == 3

    def test_get_all(self):
        response = self.client.get('/')

        assert response.status_code == 200
        assert len(response.context['games']) == 3
        assert response.context['games'][0].id == 1
        assert response.context['games'][1].id == 2
        assert response.context['games'][2].id == 3

    def test_create_new(self):
        response = self.client.post('/new')
        self.assertRedirects(response, '/%d/' % (self.max_id+1))

    def test_get_game(self):
        response = self.client.get('/1/')

        assert response.status_code == 200
        assert type(response.context['game']) == Game

    def test_post_move(self):
        response = self.client.post('/1/move',
                                    {'player': 'x', 'col': 0, 'row': 0})
        self.assertRedirects(response, '/1/')

        response = self.client.get('/1/')

        assert response.status_code == 200
        assert type(response.context['game']) == Game
        assert response.context['game'][0][0] == PLAYER_X

    def test_post_move_by_ajax(self):
        response = self.client.post('/2/move',
                                    {'player': 'x', 'col': 0, 'row': 0},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                                    )
        assert response.status_code == 200
        content = json.loads(response.content)
        assert content['player'] == 'o'
        assert 'col' in content
        assert 'row' in content
