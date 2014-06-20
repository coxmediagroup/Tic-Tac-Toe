from functools import partial

from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APISimpleTestCase


class TestAPIGamePlayView(APISimpleTestCase):
    
    def setUp(self):
        super(TestAPIGamePlayView, self).setUp()
        self.api_client = APIClient()
        # use this shortcut
        self.post_to_play_endpoint = partial(self.api_client.post,
                                             reverse('tic_tac_toe:play-game'),
                                             format='json')
    
    def test_game_play_x_wins(self):
        data = {'board': [None,'X','O','X','X',None,None,'O','O']}
        resp = self.post_to_play_endpoint(data=data)
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        # expected response board
        x_wins_board = {
            'board': (None, 'X', 'O', 'X', 'X', 'X', None, 'O', 'O'),
            'status': 'WIN',
            'winner': 'X'
        }
        self.assertDictEqual(resp.data['data'], x_wins_board)
        self.assertTrue(resp.data['success'])
    
    def test_game_play_its_a_draw(self):
        data = {'board': ['O','X','O','X','X','O','O','O',None]}
        resp = self.post_to_play_endpoint(data=data)
        # expected response board
        x_wins_board = {
            'board': ('O','X','O','X','X','O','O','O','X'),
            'status': 'DRAW',
        }
        self.assertDictEqual(resp.data['data'], x_wins_board)
        self.assertTrue(resp.data['success'])
    
    def test_response_400_when_supplied_bad_data(self):
        """cannot create games with bad data"""
        # case 1: invalid board length
        invalid_length_board = {'board': ['X',None,None,'O','O']}
        resp = self.post_to_play_endpoint(data=invalid_length_board)
        self.assertFalse(resp.data['success'])
        self.assertEquals(resp.status_code, status.HTTP_400_BAD_REQUEST)
        
        # case 2: invalid symbols
        invalid_length_board = {'board': ['.','+','#','X','X','O','O','O','X']}
        resp = self.post_to_play_endpoint(data=invalid_length_board)
        self.assertFalse(resp.data['success'])
        self.assertEquals(resp.status_code, status.HTTP_400_BAD_REQUEST)