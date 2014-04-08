from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import RequestFactory

from .models import Game
from .views import home, make_move, new_game

import json

class ClientViews(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_home(self):
        url = reverse('home')
        request = self.factory.get(url)
        response = home(request)

        self.assertEqual(200, response.status_code)
        self.assertIn("Tic Tac Toe by Jack Slingerland", response.content)

    def test_make_move_with_invalid_parameters(self):
        url = reverse('make-move')
        request = self.factory.post(url)
        response = make_move(request)

        self.assertEqual(200, response.status_code)
        self.assertEqual({
            'error' : 'You are missing a required parameter.'
        }, json.loads(response.content))

    def test_make_move_with_valid_parameters(self):

        game = Game(name='Test Game')
        game.save()

        url = reverse('make-move')
        request = self.factory.post(url, {
            'board' : ',O,X,,X,,,,',
            'game' : game.id,
            'x' : 2,
            'y' : 1
        })
        response = make_move(request)

        self.assertEqual(200, response.status_code)
        self.assertNotIn('error', response.content)
        self.assertEqual(None, json.loads(response.content)['state'])
        self.assertNotEqual(None, json.loads(response.content)['coordinates'])

    def test_new_game_with_invalid_parameters(self):
        url = reverse('new-game')
        request = self.factory.post(url)
        response = new_game(request)

        self.assertEqual(200, response.status_code)
        self.assertEqual({
            'error' : "'name' field is required."
        }, json.loads(response.content))

    def test_new_game_with_valid_parameters(self):
        url = reverse('new-game')
        request = self.factory.post(url, { 'name' : 'Jack' })
        response = new_game(request)

        self.assertEqual(200, response.status_code)
        self.assertNotIn('error', response.content)
        self.assertEqual(Game.objects.get(name='Jack').id, json.loads(response.content)['id'])
