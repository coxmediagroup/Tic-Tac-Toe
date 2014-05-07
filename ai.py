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
	#this will check for posible moves.
		global matrix
		global wins

		if self.matrix is None:
			self.matrix = omatrix

		matrix = self.matrix
		combo = 0
		moves = dict()
		compw = False
		playerw = False
		for win in self.wins:
			combo = combo + 1
			score = 0
			owner = None
			mtx = set()

			for key in win:	
				key = str(key)
				mtx.add(matrix[key])

				score = score + int(matrix[key])
				if matrix[key] == 0:
					moves[combo] = [int(key), combo]

			if score == 4:	
				if all(e in mtx for e in (0,)):
					owner = 'COUNTER IT!'
					moves[combo].extend(['counter'])

			if score == 3:
				if all(e in mtx for e in (2,)):
					owner = 'mixed'
					moves[combo].extend(['open'])
				else:
					compw = True

			if score == 2:
				if all(e in mtx for e in (1,)):
					owner = 'MOVE!'
					moves[combo].extend(['win'])

			if score == 1:
				owner = 'Find Move'
				moves[combo].extend(['potential'])

			if score == 5:
				owner = 'full'

			if score == 6:
				playerw = True

		output = None
		typ = None
		op = False
		pot = False
		cntr = False
		win = False

		opm = None
		potm = None
		cntrm = None
		winm = None

		for key, value in moves.iteritems():
			value = list(value)
						
			if 'open' in value:
				op = True
				opm = value[0]

			if 'potential' in value:
				pot = True
				potm = value[0]
			
			if 'win' in value:
				win = True
				winm = value[0]
				break
			
			if 'counter' in value:
				cntr = True
				cntrm = value[0]

		if win:
			output = winm
			typ = "win"
		elif cntr:
			output = cntrm
			typ = "counter"
		elif pot:
			output = potm
			typ = "potential"
		elif op:
			output = opm
			typ = "open"
		else:
			if compw:
				output = 0
				typ = "Comp Wins!"
			elif playerw:
				output = 0
				typ = "Player Wins... Wahhh!!???"
			else:
				output = 0
				typ = "cat"

		# This prints out what the final output should be.
		print "***********"
		print output
		print typ
		print "***********"
