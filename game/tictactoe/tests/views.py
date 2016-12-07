import json

from django.core.urlresolvers import reverse
from django.test import TestCase
from nose.tools import eq_


class TestView(TestCase):

    def setUp(self):
        pass

    def test_play(self):
        res = self.client.get(reverse('tictactoe.play'))
        eq_(res.status_code, 200)
        assert res.context['corner'] != -1

    def test_play_human(self):
        res = self.client.get('%s?start=human' % reverse('tictactoe.play'))
        eq_(res.status_code, 200)
        eq_(res.context['corner'], -1)

    def test_make_move_invalid(self):
        form = {'move': ''}
        res = self.client.post(reverse('tictactoe.make_move'), form)
        res = json.loads(res.content)
        self.assertFalse(res['success'])

    def test_make_move_valid(self):
        res = self.client.get(reverse('tictactoe.play'))
        form = {'move': '4'}
        res = self.client.post(reverse('tictactoe.make_move'), form)
        eq_(res.status_code, 200)
        res = json.loads(res.content)
        self.assertTrue(res['success'])
