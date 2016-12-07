"""
The Tic Tac Toe logic
"""

import json, random

class TicTacToe :
	EMPTY_DATA = 0
	PLAYER1_DATA = 1
	PLAYER2_DATA = 2

	def __init__(self, player_name=None, human_first=True):
		self.player_name = player_name
		self.human_first = human_first

		self.reset()

	def reset(self, player_name=None, human_first=None):
		if player_name is not None:
			self.player_name = player_name
		if human_first is not None:
			self.human_first = human_first

		self.human_data    = TicTacToe.PLAYER1_DATA if self.human_first else TicTacToe.PLAYER2_DATA
		self.computer_data = TicTacToe.PLAYER2_DATA if self.human_first else TicTacToe.PLAYER1_DATA

		self.cells = [	0,0,0,
						0,0,0,
						0,0,0]
		self.moves = []

	@staticmethod
	def from_json(txt):
		ttt = TicTacToe()
		ttt.__dict__ = json.loads(txt)
		return ttt

	def to_json(self):
		return json.dumps(self.__dict__)

	def occupied(self, cell):
		return self.cells[cell-1] != 0

	def record_move(self, cell, player):
		if cell is not None:
			self.moves.append(cell)
			self.cells[cell-1] = player
		return cell

	def record_human_move(self, cell):
		return self.record_move(cell, self.human_data)

	def record_computer_move(self, cell):
		return self.record_move(cell, self.computer_data)

	def do_first_move(self):
		"Run the first move if the human refuses to go first"

		if not self.human_first:
			move = self._computer_first_move()
			return self.record_computer_move(move)
		return None

	def do_move(self):
		"Find our next move"

		move = self._get_move_win()
		if move:
			return self.record_computer_move(move)

		move = self._get_move_block()
		if move:
			return self.record_computer_move(move)

		if not self.human_first:
			move = self._computer_first_move()
		else:
			move = self._human_first_move()

		return self.record_computer_move(move)


	def _get_move_name(self):
		"A string representation of all moves performed"

		moveName = ""

		for move in self.moves:
			moveName += str(move)

		if moveName is "":
			moveName = "-"

		return moveName

	def _get_taken_cells(self):
		"cells already taken in play"

		taken = []
		for i in range(0, 9):
			if self.cells[i] is not 0:
				taken.append(i+1)

		return taken

	def _pick_move(self, bestMoves):
		print "all best: "
		print bestMoves

		moveName = self._get_move_name()
		taken = self._get_taken_cells()

		# exact try
		possibleMoves = bestMoves.get(moveName)

		if possibleMoves is None and len(moveName) > 1:
			# try partial -1
			possibleMoves = bestMoves.get(moveName[:-1])

		if possibleMoves is None and len(moveName) > 2:
			# try partial -2
			possibleMoves = bestMoves.get(moveName[:-2])

		if possibleMoves is None:
			# was it a late center move?
			if len(moveName) >= 4 and moveName[3] == '5':
				moveName = moveName[0] + "xx5"
				possibleMoves = bestMoves.get(moveName)

		print "possible: "
		print possibleMoves

		if possibleMoves is not None:
			# now we have good moves to try, remove taken cells
			possibleMoves = list( set(possibleMoves) - set(taken) )

			if len(possibleMoves) == 1:
				return possibleMoves[ 0 ];

			# randomize the next move so user thinks they have a chance
			if len(possibleMoves) > 1:
				return possibleMoves[ random.randint(0, len(possibleMoves)-1) ];

			# else fall down to brute force

		# brute force into TIE
		for j in range(0, 9):
			if self.cells[j] == TicTacToe.EMPTY_DATA:
				return j+1

		# TIE
		return None

	def _computer_first_move(self):

		# map of current taken moves to an array of good moves
		# this is structured so that if a perfect match is not found then a partial match can be good too
		bestMoves = {
			# start
			"-": [5,1,3,7,9],

			# center -> corner
			"51": [9],
			"53": [7],
			"57": [3],
			"59": [1],

			"519": [7,3],
			"537": [1,9],
			"573": [1,9],
			"591": [7,3],

			# center -> edge
			"52": [7,9],
			"54": [3,9],
			"56": [1,7],
			"58": [1,3],

			# 5273  [9]
			# 527x  [3]
			# 5291  [7]
			# 529x  [1]

			# corner -> center
			"15": [9],
			"35": [7],
			"75": [3],
			"95": [1],

			"159": [3,7],
			"357": [1,9],
			"753": [1,9],
			"951": [3,7],

			# corner -> edge / corner
			"12": [7,9],
			"13": [7,9],
			"14": [3,9],
			"17": [3,9],
			"16": [3,7,9],
			"18": [3,7,9],
			"19": [3,7],

			"31": [7,9],
			"32": [7,9],
			"34": [1,7,9],
			"36": [1,7],
			"37": [1,9],
			"38": [1,7,9],
			"39": [1,7],

			"71": [3,9],
			"72": [1,3,9],
			"73": [1,9],
			"74": [3,9],
			"76": [1,3,9],
			"78": [1,3],
			"79": [1,3],

			"91": [3,7],
			"92": [1,3,9],
			"93": [1,7],
			"94": [1,3,7],
			"96": [1,7],
			"97": [1,3],
			"98": [1,3],

			# psuedo match after partials fail to pick up common case of center taken later
			"1xx5": [3,7],
			"3xx5": [1,9],
			"7xx5": [1,9],
			"9xx5": [3,7]
		}

		return self._pick_move(bestMoves)

	def _human_first_move(self):

		bestMoves = {
			# start
			"-": [5], # actually should NEVER occur 
			"5": [1,3,7,9],

			"1": [5],
			"3": [5],
			"7": [5],
			"9": [5],

			"159": [2,4,6,8],
			"357": [2,4,6,8],
			"753": [2,4,6,8],
			"951": [2,4,6,8],

			"15": [3,7,9],
			"35": [1,7,9],
			"75": [1,3,9],
			"95": [1,3,7]
		}

		return self._pick_move(bestMoves)

	def _tally_row(self, cells):
		row = [ 
		  self.cells[cells[0]-1] , 
		  self.cells[cells[1]-1] , 
		  self.cells[cells[2]-1] ]

		tally = [0,0,0] # empty, computer, human

		for i in [0,1,2]:
			if row[i] == 0: 
				tally[0] = cells[i] # ok, ok, empty is not a count but last found empty cell
			elif row[i] == self.computer_data:
				tally[1] += 1
			else:
				tally[2] += 1
		print tally
		return tally

	def _check_for_block(self, cells):
		tally = self._tally_row(cells)
		if tally[2] == 2 and tally[1] == 0:
			return tally[0]
		return None

	def _check_for_win(self, cells):
		tally = self._tally_row(cells)
		if tally[1] == 2 and tally[2] == 0:
			return tally[0]
		return None

	def _get_move_block(self):
		for cell in [1,2,3,4,7]:
			player = self.cells[cell-1]
			print "check block cell %d player %s" % (cell, (player))

			if player is not self.computer_data:
				if cell in [1,2,3]: #vertical
					print "vert"
					move = self._check_for_block([cell + 0, cell + 3, cell + 6])
					if move:
						return move
				if cell in [1,4,7]: #horizontal
					print "horz"
					move = self._check_for_block([cell + 0, cell + 1, cell + 2])
					if move:
						return move

				if cell is 1: # diagonal
					print "diag 1"
					move = self._check_for_block([1,5,9])
					if move:
						return move
				if cell is 3: # diagonal
					print "diag 2"
					move = self._check_for_block([3,5,7])
					if move:
						return move
		return None

	def _get_move_win(self):
		for cell in [1,2,3,4,7]:
			print "check to win cell %d" % (cell)
			if True:
				if cell in [1,2,3]: #vertical
					print "vert"
					move = self._check_for_win([cell + 0, cell + 3, cell + 6])
					if move:
						return move

				if cell in [1,4,7]: #horizontal
					print "horz"
					move = self._check_for_win([cell + 0, cell + 1, cell + 2])
					if move:
						return move
				if cell is 1: # diagonal
					print "diag 1"
					move = self._check_for_win([1,5,9])
					if move:
						return move
				if cell is 3: # diagonal
					print "diag 2"
					move = self._check_for_win([3,5,7])
					if move:
						return move
		return None

	def did_player_win(self):
		for cell in [1,2,3,4,7]:
			player = self.cells[cell-1]
			print "check cell %d player %s" % (cell, (player))
			if player is not 0:
				if cell in [1,2,3]: #vertical
					print "vert"
					if self.cells[cell-1 + 3] == player and self.cells[cell-1 + 6] == player:
						return player
				if cell in [1,4,7]: #horizontal
					print "horz"
					if self.cells[cell-1 + 1] == player and self.cells[cell-1 + 2] == player:
						return player
				if cell is 1: # diagonal
					print "diag 1"
					if self.cells[5-1] == player and self.cells[9-1] == player:
						return player
				if cell is 3: # diagonal
					print "diag 2"
					if self.cells[5-1] == player and self.cells[7-1] == player:
						return player
		return None

	def did_tie(self):
		found = False
		for j in range(0, 9):
			if self.cells[j] == 0:
				found = True
		return not found
