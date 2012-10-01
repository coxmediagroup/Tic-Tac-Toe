from copy import deepcopy

from django.test import TestCase

import game

class GameViewTestCase(TestCase):
    """
    Test GET and POST requests
    """
    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('gameboard' in response.context)
        
    def test_post_move(self):
        response = self.client.post('/', {'move': 1, 'position': '11'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('gameboard' in response.context)
        self.assertEqual(response.context['gameboard'].boardstate[1][1], 1)
        # Duplicate move
        response = self.client.post('/', {'move': 1, 'position': '11'})
        self.assertTrue('message' in response.context)
        
    def test_reset(self):
        response = self.client.post('/', {'move': 1, 'position': '11'})
        response = self.client.post('/', {'reset': 1})
        self.assertEqual(response.context['gameboard'].boardstate, \
                         [[0,0,0],[0,0,0],[0,0,0]])
        
class GameboardTestCase(TestCase):
    """
    Test Gameboard methods
    """
    def setUp(self):
        self.gameboard = game.Gameboard()
        self.gameboard.boardstate = [[-1,1,1],[-1,0,1],[-1,0,0]]
        
    def test_available_spaces(self):
        self.assertEqual(self.gameboard.available_spaces(), [[1,1],[2,1],[2,2]])
        
    def test_check_status(self):
        self.assertFalse(self.gameboard.check_status(1))
        self.assertTrue(self.gameboard.check_status(-1))
        self.assertEqual(self.gameboard.status, 'Computer wins!')
        
    def test_save_move(self):
        self.gameboard.save_move([2,2], 1)
        self.assertEqual(self.gameboard.boardstate[2][2], 1)
        self.gameboard.save_move([2,2], 0)
        self.assertEqual(self.gameboard.boardstate[2][2], 0)
        
    def test_sum_rows(self):
        self.assertEqual(self.gameboard._sum_rows([0,0,0]), 0)
        self.assertEqual(self.gameboard._sum_rows([0,0,1]), 1)
        self.assertEqual(self.gameboard._sum_rows([-1,0,1]), 0)
        self.assertEqual(self.gameboard._sum_rows([-1,0,0]), -1)
        self.assertEqual(self.gameboard._sum_rows([-1,-1,0]), -10)
        self.assertEqual(self.gameboard._sum_rows([-1,-1,-1]), -100)
        self.assertEqual(self.gameboard._sum_rows([1,0,0]), 1)
        self.assertEqual(self.gameboard._sum_rows([1,1,0]), 10)
        self.assertEqual(self.gameboard._sum_rows([1,1,1]), 100)

class ComputerWinsTestCase(TestCase):
    """
    Test all possible game outcomes to ensure computer doesn't lose
    """
    def setUp(self):
        self.gameboard = game.Gameboard()
        
    def test_all_moves(self):
        def _move(gameboard):
            for position in gameboard.available_spaces():
                snapshot = deepcopy(gameboard)
                snapshot.save_move(position, 1)
                snapshot.check_status(1)
                if snapshot.status == 'Game ends in a draw!':
                    break
                self.assertFalse(snapshot.status)
                snapshot.computer_move()
                snapshot.check_status(-1)
                if snapshot.status == 'Computer wins!':
                    break
                _move(snapshot)
                
        _move(self.gameboard)
