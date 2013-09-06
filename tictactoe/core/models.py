import datetime

from django.contrib.auth.models import User
from django.db import models

GAME_STATUS = (('won', 'Won'), ('lost', 'Lost'), ('tied', 'Tied'), ('in_progress', 'In Progress'))

class GameHistory(models.Model):
    start_datetime = models.DateTimeField(auto_now_add=True)
    end_datetime = models.DateTimeField(null=True, blank=True)
    player = models.ForeignKey(User)
    status = models.CharField(choices=GAME_STATUS, default='in_progress', max_length=30)

    def finish_game(self, result):
        self.status = result
        self.end_datetime = datetime.datetime.now()
        self.save()
