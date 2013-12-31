"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from game import models

class SimpleTest(TestCase):
    def setUp(self):
        self.new_game = models.SingleGame()
        self.new_game.save()

    def test_unused_squares(self):
        state = '0P,1C,2C,3P,4P,5C,6P,7C'
        self.assertEqual(self.new_game.get_unused_squares(state), [8])
        state = '8P,1C,2C,3P,4P,5C,6P,7C'
        self.assertEqual(self.new_game.get_unused_squares(state), [0])
        state = '0P,1C,2C,3P,8P,5C,6P,7C'
        self.assertEqual(self.new_game.get_unused_squares(state), [4])
        
