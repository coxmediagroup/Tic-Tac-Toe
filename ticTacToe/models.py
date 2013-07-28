from django.db import models

# Create your models here.
class Players(models.Model):
	id = models.AutoField(primary_key = True)
	name = models.CharField(max_length = 100)
	
	def __unicode__(self):
		return self.name + ' (id: ' + str(self.id) + ')' 

class Games(models.Model):
	id = models.AutoField(primary_key = True)
	playerOne = models.ForeignKey(Players, related_name = 'Player1')
	playerTwo = models.ForeignKey(Players, related_name = 'Player2')
	startTime = models.DateTimeField()
	
	def __unicode__(self):
		return playerTwo.name + ' vs ' + playerTwo.name + ' (id: ' + \
			str(self.id) + ')'

class Moves(models.Model):
	id = models.AutoField(primary_key = True)
	game = models.ForeignKey(Games)
	player = models.ForeignKey(Players)
	positionX = models.IntegerField()
	poxitionY = models.IntegerField()
	timestamp = models.DateTimeField()
	
	def __unicode__(self):
		return player.name + ' took [' + str(self.positionX) + ', ' + \
			str(self.positionY) + '] (id: ' + str(self.id) + ')' 
