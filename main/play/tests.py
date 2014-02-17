from django.utils import unittest
from django.test.client import Client
import re
class BoardTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_getDefaultBoard(self):
        # Issue a GET request.
        response = self.client.get('/')
        blank_board = ['','','','','X','','','','']

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        #check the string returned for a blank request
        self.assertEqual(response.context['board'],blank_board)

