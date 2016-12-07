from django.db import models

class Player(models.Model):
    """ Model representing a player """

    email = models.EmailField()
    full_name = models.CharField(max_length=120)
    total_plays = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)

    def __unicode__(self):
        return self.email

