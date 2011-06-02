from django.test import TestCase
import sys

class GameTestCase(TestCase):
	def test_game(self):
		import ipdb; ipdb.set_trace()
		response = self.client.get('/', follow=True)
		self.assertEqual(response.status_code, 200)
		
		response = self.client.get('/pick/2', follow=True)
		self.assertEqual(response.status_code, 200)
		response = self.client.get('/move/2', follow=True)
		self.assertEqual(response.status_code, 200)
		response = self.client.get('/move/8', follow=True)
		self.assertEqual(response.status_code, 200)
		response = self.client.get('/move/3', follow=True)
		self.assertEqual(response.status_code, 200)