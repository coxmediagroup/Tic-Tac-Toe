from django.db import models


class Game(models.Model):
    user = models.ForeignKey('auth.User')
    timestamp = models.DateTimeField(auto_now_add=True)
