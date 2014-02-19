from django.utils import unittest
from django.test.client import Client
import re
from tictactoe.tictactoe import Player, AIPlayer, Board
import simplejson

class BoardTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.blank_board = Board(the_board=[None, None, None, None, u'X', None, None, u'O', None])

    def test_getDefaultBoard(self):
        # Issue a GET request.
        response = self.client.get('/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        #check the string returned for a blank request is what we expect
        self.assertEqual(response.context['the_board'],self.blank_board)



class PlayerTest(unittest.TestCase):

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        #the aiPlayer to compare against
        self.aiPlayer = AIPlayer('X')
        #the human player to compare against
        self.humanPlayer = Player('O')
        self.initial_state = [None, None, None, None, u'X', None, None, u'O', None]

    def test_MakeHumanPlayerO(self):
        # Issue a GET request.
        response = self.client.get('/?board=' + simplejson.dumps(self.initial_state))

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        #check the string returned for a blank request
        self.assertEqual(response.context['human'].board_value,'O')

    def test_MakeAIPlayerX(self):
        # Issue a GET request.
        response = self.client.get('/?board=' + simplejson.dumps(self.initial_state))

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        #check the string returned for a blank request
        self.assertEqual(response.context['human'].board_value,'O')
