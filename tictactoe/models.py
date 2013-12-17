from django.core.urlresolvers import reverse
from django.db import models


class Game(models.Model):
    user = models.ForeignKey('auth.User')
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('game_detail', kwargs={'pk': self.pk})
