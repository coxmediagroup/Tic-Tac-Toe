from random import randint
import json

class gen():
	def rand(self, ceil):
		return randint(1, ceil)
		# return ceil

class comp():
	matrix = None # Global matrix container

	wins = [
		[7,8,9], # top row
		[4,5,6], # middle row
		[1,2,3], # bottom row
		[1,5,9], # asc diagonal
		[7,5,3], # desc diagonal
		[7,4,1], # left column
		[8,5,2], # middle column
		[9,6,3], # right column
	]

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

	def check_for_win(self, omatrix = None):
	#this will check for any posible winning moves.
		global matrix
		global wins

		if self.matrix is None:
			self.matrix = omatrix

		matrix = self.matrix
		print matrix['1']

		for win in self.wins:
			# win = str(win)
			score = 0
			owner = None
			mtx = set()
			for key in win:	
				key = str(key)
				mtx.add(matrix[key])
				print matrix[key]
				score = score + int(matrix[key])

			# if any(e in win for e in (1,1,0)):	
			# 	owner = 'compwin'

			if score == 4:	
				if all(e in mtx for e in (1,)):
					owner = 'full'
				else:
					owner = 'COUNTER IT!'

			if score == 3:
				if all(e in mtx for e in (2,)):
					owner = 'mixed'
				else:
					owner = 'I WIN!'

			if score == 2:
				if all(e in mtx for e in (0,)):
					owner = 'MOVE!'
				else:
					owner = 'Find Move'

			if score == 1:
				owner = 'Find Move'

			if score == 5:
				owner = 'full'

			if score == 6:
				owner = "ERROR!"



			print str(win) + ' | ' + str(score) + ' | ' + str(owner)

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

	def check_for_counter(self, omatrix = None):
	# This will check for a proper counter move.
		global matrix

		if self.matrix is None:
			self.matrix = omatrix

		counter = None

		#logic for counter move goes here.
		return counter