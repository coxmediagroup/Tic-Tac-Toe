import random
import json

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

	def findPreferred(self, matrix):
		corner = [1,3,7,9]
		edge = [2,4,6,8]
		fm = None
		total = 0
		cornerm = random.choice(corner);
		edgem = random.choice(edge);
		centerm = 5

		if matrix['5'] == 2:			
			preferred = [centerm, cornerm, edgem]
		else:
			preferred = [centerm, edgem, cornerm]
			
		output = 0

		for key in preferred:
			key = str(key)

			if matrix[key] == 0:
				output = key
				break

		return output

	def next_move(self, omatrix = None):
	#this will check for posible moves.
		global matrix
		global wins

		if self.matrix is None:
			self.matrix = omatrix

		matrix = self.matrix
		matrix = json.loads(matrix)
		combo = 0
		moves = dict()
		compw = False
		playerw = False

		for win in self.wins:
			combo = combo + 1
			score = 0
			mtx = set()
			total = 0

			for key in win:	
				key = str(key)
				mtx.add(matrix[key])

				score = score + int(matrix[key])
				total = total + score

				if matrix[key] == 0:
					moves[combo] = [int(key), combo]

			if score == 4:	
				if all(e in mtx for e in (0,)):
					moves[combo].extend(['counter'])

			if score == 3:
				if all(e in mtx for e in (2,)):
					moves[combo].extend(['open'])
				else:
					compw = True

			if score == 2:
				if all(e in mtx for e in (1,)):
					moves[combo].extend(['win'])
				elif all(e in mtx for e in (2,)):
					moves[combo].extend(['open'])

			if score == 1:
				# moves[combo].extend(['potential'])
				moves[combo].extend(['open'])

			# if score == 5:

			if score == 6:
				playerw = True

		output = None
		typ = None

		op = False
		pot = False
		cntr = False
		win = False
		cat = False

		opm = None
		potm = None
		cntrm = None
		winm = None
		catm = None

		for key, value in moves.iteritems():
			value = list(value)
						
			if 'open' in value:
				if total < 13:
					op = True
					opm = self.findPreferred(matrix);
				else:
					cat =True
					catm = 0

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
		elif compw:
			output = 0
			typ = "Comp Wins!"
		elif playerw:
			output = 0
			typ = "Player Wins... Wahhh!!???"
		elif cat:
			output = 0
			typ = "cat"

		# This returns what the final output should be.
		finaldict = {'move':str(output), 'type':typ}
		finaljson = json.dumps(finaldict)
		return finaljson
