from random import randint

class gen():
	def rand(self, ceil):
		# return randint(1, ceil)
		return ceil

class comp():
	matrix = None # Global matrix container

	def next_move(self, player, omatrix):
	# This is where the computer figures out were to move.
		global matrix
		self.matrix = omatrix
		win = self.check_for_win();

		if win is None:
			move = int(player) - 1;
			return move
		else:
			return win

	def check_for_win(self):
	#this will check for any posible winning moves.
		global matrix
		win = None
		# Logic to detect a winning move goes here.
		win = 3

		# Logic to determine who's winning move it is goes here.
		win_owner = 2

		if win_owner == 1:
			return win
		else:
			counter = self.check_for_counter()
			return counter

	def check_for_counter(self):
	# This will check for a proper counter move.
		global matrix
		counter = None

		#logic for counter move goes here.
		return counter