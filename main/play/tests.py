from django.utils import unittest
from django.test.client import Client
import re
class BoardTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_getBlank(self):
        # Issue a GET request.
        response = self.client.get('/')
        blank_board ="""<div class="row-fluid">
            <div class="offset1 span3 well">
                <h1 class="text-center"></h1>
            </div>
            <div class="span3 well">
               <h1 class="text-center"></h1>
            </div>
            <div class="span3 well">
                <h1 class="text-center"></h1>
            </div>
        </div>
        <div class="row-fluid">
            <div class="offset1 span3 well">
                <h1 class="text-center"></h1>
            </div>
            <div class="span3 well">
               <h1 class="text-center"></h1>
            </div>
            <div class="span3 well">
                <h1 class="text-center"></h1>
            </div>
        </div>
        <div class="row-fluid">
            <div class="offset1 span3 well">
               <h1 class="text-center"></h1>
            </div>
            <div class="span3 well">
                <h1 class="text-center"></h1>
            </div>
            <div class="span3 well">
                <h1 class="text-center"></h1>
            </div>
        </div>"""

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        #check the string returned for a blank request
        #self.failUnlessAlmostEqual(response.context['da_board'],blank_board)

