from django.test import TestCase

class GameTestCase(TestCase):
	def test_game(self):
		import ipdb; ipdb.set_trace()
		response = self.client.get('/', follow=True)
		self.assertEqual(response.status_code, 200)