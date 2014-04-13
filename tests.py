import unittest
import re
from contextlib import contextmanager

from flask import json

from app import app, COOKIE_GAME_ID, session


@contextmanager
def game():
    with app.test_client() as client:
        client.get('/start')
        yield client
        client.get('/end')



class ApiTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True

    def test_session(self):
        with game():
            assert COOKIE_GAME_ID in session
            assert re.search(r'^[0-9a-f]{32}$', session[COOKIE_GAME_ID])

    def test_move_args(self):
        with game() as client:
            bad_queries = ['/move', '/move?x=1', '/move?y=1', '/move?x=1&y=a', '/move?x=-1&y=1',
                           '/move?x=2&y=4', '/move?x=3&y=1.3', '/move?x=3&y=1a']
            for query in bad_queries:
                resp = client.get(query)
                data = json.loads(resp.data)
                assert data['success'] == False 
                assert data['error'] == 'wrong_arguments' 

            resp = client.get('/move?x=0&y=2')
            data = json.loads(resp.data)
            assert data['success'] == True

    def test_twice_cell_choice(self):
        with game() as client:
            query = '/move?x=0&y=2'

            resp = client.get(query)
            data = json.loads(resp.data)
            assert data['success'] == True
            
            resp = client.get(query)
            data = json.loads(resp.data)
            assert data['success'] == False
            assert data['error'] == 'cell_taken'


    def test_game_not_started(self):
        with app.test_client() as client:
            resp = client.get('/move?x=0&y=2')
            data = json.loads(resp.data)
            assert data['success'] == False
            assert data['error'] == 'not_initiated'


if __name__ == '__main__':
    unittest.main()