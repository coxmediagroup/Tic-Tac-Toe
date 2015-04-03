import random

from django.core.urlresolvers import reverse
from django.test import TestCase

from game.models import Game


class ViewsTest(TestCase):
    def test_index_redirect(self):
        "Tests the redirection from the index URL"

        response = self.client.get(reverse('index'))
        self.assertRedirects(response, reverse('game:index'), status_code=301)

    def test_index(self):
        "Views the game index page. Not much here right now."

        response = self.client.get(reverse('game:index'))
        self.assertTemplateUsed(response, 'game/game_list.html')

    def test_index_post(self):
        "Posting to the index view gives you a new game."
        random.seed(0)

        response = self.client.post(reverse('game:index'), {
            'player1': 'game.players.AIPlayer',
            'player2': 'human'
        })
        self.assertEqual(Game.objects.count(), 1)
        game = Game.objects.all()[0]
        self.assertRedirects(response, game.get_absolute_url())

        # Players are assigned. The player should have played.
        self.assertEqual(game.board, "      X  ")
        self.assertEqual(game.player_x, 'game.players.AIPlayer')
        self.assertEqual(game.player_o, 'human')

    def test_detail(self):
        "Views the game detail page."

        game = Game.objects.create()
        response = self.client.get(game.get_absolute_url())
        self.assertTemplateUsed(response, 'game/game_detail.html')

    def test_detail_post(self):
        "Posting to the detail view plays a square."
        random.seed(0)

        game = Game.objects.create(player_x='human', player_o='game.players.AIPlayer')
        response = self.client.post(game.get_absolute_url(), {
            'index': 0
        })
        self.assertRedirects(response, game.get_absolute_url())
        # Reload the game. Both the human and random player should have played.
        game = Game.objects.get(pk=game.pk)
        self.assertEqual(game.board, "X      O ")
