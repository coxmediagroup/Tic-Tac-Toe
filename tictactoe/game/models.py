from django.db import models

from django.contrib.auth.models import User as DjangoUser

class Game(models.Model):

	"""
	Game model keep track of game board state for a tic-tac-toe game.
	
	Fields:
		board a 9 character string, each of the 9 positin can hold:
		'X' or 'O', this state that the space is played.
		' ' means the space is available.
		The board also will keep the winnings position, and will
		show the winner of the game

		date_created keep track of when game initiated
		date_updated keep track of when game finished
	"""

	#TicTacTow winning matrix
	WINS = (
		(0,1,2),
		(3,4,5),
		(6,7,8),
		(0,3,6), 
		(1,4,7),
		(2,5,8),
		(0,4,8), 
		(2,4,6)
	)

	xplayer	 		= models.CharField(max_length=64)
	oplayer	 		= models.CharField(max_length=64)
	board 			= models.CharField(max_length=9, default=" ")
	
	date_created 	= models.DateTimeField(auto_now_add=True)
	date_updated 	= models.DateTimeField(auto_now=True)
	
	def __unicode__(self):
		return '%s vs %s, board="%s"' % (self.xplayer,
										 self.oplayer,
										 self.board)

class PlayerProfile(models.Model):
	
	PLAYER_TYPE_CHOICES =((0,'Computer'), (1,'Human'))
	
	player           	= models.ForeignKey(DjangoUser, unique=True)
	player_type      	= models.IntegerField(choices=PLAYER_TYPE_CHOICES,
											  default=1,
											  max_length=1)
	total_games_won		= models.IntegerField(default=0)
	total_games_lost	= models.IntegerField(default=0)
	total_games_draw	= models.IntegerField(default=0)

	def __unicode__(self):
		return '%s %s (%s)' % (self.player.first_name,
							   self.player.last_name,
							   self.get_player_type_display())

	def save(self, **kwargs):
		super(PlayerProfile, self).save(**kwargs)