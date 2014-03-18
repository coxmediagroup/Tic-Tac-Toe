import unittest
import json

import app


class TestViews(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()

    def test_ai_first(self):
        resp = self.app.get('/ai_first/')
        actual = json.loads(resp.data)
        self.assertIn(actual['mark_cell'], ['c1', 'c3', 'c7', 'c9'])
