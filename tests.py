import unittest
import re
from contextlib import contextmanager

from flask import json

from app import app, COOKIE_GAME_ID, session
from game import Game


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

    def test_ia_turn(self):
        with game() as client:
            resp = client.get('/move?x=1&y=2')
            data = json.loads(resp.data)
            assert 'game_over' in data
            assert data['game_over'] == False
            assert 'ai_move' in data
            assert isinstance(data['ai_move'], dict) 
            assert data['ai_move']['x'] in range(Game.BOARD_SIZE) 
            assert data['ai_move']['y'] in range(Game.BOARD_SIZE) 
            

if __name__ == '__main__':
    unittest.main()