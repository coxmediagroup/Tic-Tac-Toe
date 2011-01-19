"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""
from django.contrib.auth.models import User

from django.test import TestCase
from DJTickyTack.models import Game

class GameTest(TestCase):

    def setUp(self):
        self.player1 = User.objects.create_user('player1', 'player1@example.com')
        self.player2 = User.objects.create_user('player2', 'player2@example.com')

    def test_fields(self):
        """
        A Game is a match between two players, started on a particular date.
        """
        game = Game(player1=self.player1, player2=self.player2)
        self.assertEquals(None, game.startedOn)
        game.save()
        self.assertNotEqual(None, game.startedOn)

