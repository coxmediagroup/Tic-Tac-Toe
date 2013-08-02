from django.db import models

class Games(models.Model):
	id = models.AutoField(primary_key = True)
	status = models.CharField(max_length = 20)
	playerTurn = models.BooleanField(default = True)
	startTime = models.DateTimeField()

	def __unicode__(self):
		return 'game (id: ' + str(self.id) + ')'

class Moves(models.Model):
	id = models.AutoField(primary_key = True)
	game = models.ForeignKey(Games)
	player = models.BooleanField()
	positionX = models.IntegerField()
	positionY = models.IntegerField()
	timestamp = models.DateTimeField()

	def __unicode__(self):
		if player == True:
			playerName = 'Player'
		else:
			playerName = 'Computer'

		return playerName + ' took [' + str(self.positionX) + ', ' + \
			str(self.positionY) + '] (move.id: ' + str(self.id) + \
			', game.id: ' + str(game) + ')'
