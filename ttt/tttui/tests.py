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

    def test_get_game(self):
        response = self.client.get('/1/')

        assert response.status_code == 200
        assert type(response.context['game']) == Game
