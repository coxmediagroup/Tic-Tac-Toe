from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from django.conf import settings

from .. import models


class GameCreateViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='default',
                                             password='password')
        self.create_url = reverse('create_game')

    def test_authenticated(self):
        self.assertEqual(models.Game.objects.count(), 0)
        self.client.login(username='default', password='password')

        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(self.create_url, {})
        self.assertEqual(response.status_code, 302)

        self.assertEqual(models.Game.objects.count(), 1)
        game = models.Game.objects.get()
        self.assertRedirects(response,
                             reverse('game_detail', kwargs={'pk': game.pk}))
        self.assertEqual(game.user, self.user)

    def test_anonymous(self):
        self.assertEqual(models.Game.objects.count(), 0)

        response = self.client.get(self.create_url)
        self.assertRedirects(response,
                             "{0}?next={1}".format(settings.LOGIN_URL,
                                                   self.create_url))

        response = self.client.post(self.create_url, {})
        self.assertRedirects(response,
                             "{0}?next={1}".format(settings.LOGIN_URL,
                                                   self.create_url))

        self.assertEqual(models.Game.objects.count(), 0)


class GameDetailViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='default',
                                        password='password')
        self.game = models.Game(user=self.user)
        self.game.save()

        self.detail_url = reverse('game_detail', kwargs={'pk': self.game.pk})

    def test_exists(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "default vs. the Computer")

    def test_does_not_exist(self):
        response = self.client.get(
            reverse('game_detail', kwargs={'pk': self.game.pk+1}))
        self.assertEqual(response.status_code, 404)
