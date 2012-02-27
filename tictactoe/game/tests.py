import logging

from django.test import TestCase
from django.http import HttpRequest
from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import Client


class GameViewsTest(TestCase):
    def test_index(self):
        """
        Test the index view of the application.
        """
        game_index = reverse('site-index')

        response = self.client.get(game_index)
        code = response.status_code
        expected = 200
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s'
        % (expected, code, game_index))

    def test_createGame(self):
        """
        Test the creation of the game board.
        """
        game_creation = reverse('game:createGame')

        #Get request should redirect.
        response = self.client.get(game_creation)
        code = response.status_code
        expected = 303
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s'
        % (expected, code, game_creation))

        #path = response.path
        #expected = reverse('site_index')
        #self.assertEqual(path, expected, 'Expected %s but returned %s for %s'
        #% (expected, code, game_creation))

        #Test with fully invalid form
        form_data = {'blah': 'blah',
                     'size': 3,}
        response = self.client.post(game_creation, data=form_data)
        code = response.status_code
        expected = 303
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s'
        % (expected, code, game_creation))

        #Test with valid params but invalid range input
        form_data = {'boardSize': 10,
                     'playerCharacter': 'C',}
        response = self.client.post(game_creation, data=form_data)
        code = response.status_code
        expected = 303
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s'
        % (expected, code, game_creation))

        #Test with valid params but non-integer value for size
        form_data = {'boardSize': 'y',
                     'playerCharacter': 'X',}
        response = self.client.post(game_creation, data=form_data)
        code = response.status_code
        expected = 303
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s'
        % (expected, code, game_creation))


        #Test with correct form of 3 with player 1
        form_data = {'boardSize': '3',
                     'playerCharacter': 'X',}
        response = self.client.post(game_creation, data=form_data)
        code = response.status_code
        expected = 200
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s'
        % (expected, code, game_creation))

        #Test with correct form of 4 with player 2
        form_data = {'boardSize': '4',
                     'playerCharacter': 'O',}
        response = self.client.post(game_creation, data=form_data)
        code = response.status_code
        expected = 200
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s'
        % (expected, code, game_creation))
        self.assertContains(response, 'tic_X.png', 'Expected the CPU player to have an X on the board')


