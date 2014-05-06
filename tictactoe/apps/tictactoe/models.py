from django.db import models



class Player(models.Model):
	username = models.CharField(max_length=32)
	wins = models.IntegerField(default=0)
	plays = models.IntegerField(default=0)
	first_play=models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.username
