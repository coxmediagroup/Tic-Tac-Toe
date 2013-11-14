from django.db import models

class Board(models.Model):
	"""
	This represents a standard game board. It consists of 9 boxes. Each box is
	represented by one of three states:

	0     No Game Piece
	1     Player Piece
	-1    Computer Piece
	"""
	# Top Row
	top_left = models.SmallIntegerField(default=0)
	top_center = models.SmallIntegerField(default=0)
	top_right = models.SmallIntegerField(default=0)

	# Center Row
	left = models.SmallIntegerField(default=0)
	center = models.SmallIntegerField(default=0)
	right = models.SmallIntegerField(default=0)

	# Bottom Row
	bottom_left = models.SmallIntegerField(default=0)
	bottom_center = models.SmallIntegerField(default=0)
	bottom_right = models.SmallIntegerField(default=0)

	def victory_status(self):
		"""
		This method determines the current victory status of the board. It will
		return one of the three states:

		0     Still in Progress
		1     Human has Won
		-1    Computer has Won
		"""
		# Rows
		if self.top_left == self.top_center == self.top_right \
			and self.top_left != 0:
			return self.top_left
		if self.left == self.center == self.right \
			and self.left != 0:
			return self.left
		if self.bottom_left == self.bottom_center == self.bottom_right \
			and self.bottom_left != 0:
			return self.bottom_left

		# Columns
		if self.top_left == self.left == self.bottom_left \
			and self.top_left != 0:
			return self.top_left
		if self.top_center == self.center == self.bottom_center \
			and self.top_center != 0:
			return self.top_center
		if self.top_right == self.right == self.bottom_right \
			and self.top_right != 0:
			return self.top_right

		# Diagonals
		if self.top_left == self.center == self.bottom_right \
			and self.top_left != 0:
			return self.top_left
		if self.top_right == self.center == self.bottom_left \
			and self.top_right != 0:
			return self.top_right

		# Still in Progress
		return 0

	def __unicode__(self):
		"""
		Returns a Character-Representation of the Game Board.
		"""
		text = u"\n"
		text += " %i  |  %i  |  %i\n" % (self.top_left, self.top_center, 
											self.top_right)
		text += "----------------\n"
		text += " %i  |  %i  |  %i\n" % (self.left, self.center, 
											self.right)
		text += "----------------\n"
		text += " %i  |  %i  |  %i\n" % (self.bottom_left, self.bottom_center, 
											self.bottom_right)
		return text
