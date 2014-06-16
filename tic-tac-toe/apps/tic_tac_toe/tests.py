from django.core.urlresolvers import reverse
from rest_framework import status
# from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from rest_framework.test import APISimpleTestCase


class TestAPIGamePlayView(APISimpleTestCase):
    
    def setUp(self):
        super(TestAPIGamePlayView, self).setUp()
        self.api_client = APIClient()
    
    def test_game_play(self):
        data = {}
        resp = self.api_client.post(reverse('tic_tac_toe:play-game'), data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
