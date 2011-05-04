# Tic Tac Toe
# -- classic game :)
from random import shuffle, randint

# all sets of winning possibilities--all values represent a group of 
# offsets that must be the same mark in order for a win to take place.
wins = (
	# horizontal wins
	(0, 1, 2), (3, 4, 5), (6, 7, 8),
	# vertical wins
	(0, 3, 6), (1, 4, 7), (2, 5, 8),
	# diagonal wins
	(0, 4, 8), (2, 4, 6)
)

class Board:
	'''The Tic Tac Toe playing board, data, and member functions!'''
	blank = '-'
	squares = [blank] * 9
	
	def render(self):
		'''
		Renders the Tic Tac Toe game board to the screen.
		'''
		ref = self.squares
		print ref[0], ref[1], ref[2]
		print ref[3], ref[4], ref[5]
		print ref[6], ref[7], ref[8]
		
	def place(self, mark, x, y):
		'''
		Place a mark on the game board. minimum to maximum coordinates range from 
		(0, 0) to (2, 2)
		'''
		offset = y * 3 + x
		self.squares[offset] = mark[0]
		
	def get(self, x, y):
		'''
		Returns the mark at (x, y) on our game board. If (x, y) is out of range 
		then return None.
		'''
		if x < 0 or x > 2 or y < 0 or y > 2:
			return None
		return self.squares[y * 3 + x]
		
	def blanks(self):
		'''Returns a list of all offset positions that can take a new mark.'''
		blanks = []
		for i in range(len(self.squares)):
			if self.squares[i] is self.blank:
				blanks.append(i)
		return blanks
		
	def winner(self, mark = ''):
		'''
		Determines if someone won Tic Tac Toe :D
		Returns 'X' if the X player won; 'O' if O player won.
		Returns 'T' if there was a tie
		'''
		if self.blank not in self.squares: return 'T'
		if mark == '':
			# if no mark was specified, check if X won, then check if O won
			if self.winner('X') == 'X': return 'X'
			if self.winner('O') == 'O': return 'O'
		else:
			ref = self.squares
			global wins
			for win_offsets in wins:
				num_marks = 0
				for i in win_offsets:
					if board.squares[i] == mark:
						num_marks += 1
				if num_marks == 3:
					return mark
		return None
		


def get_coords(offset):
	'''
	Returns a tuple pair of coordinates based on the game board's offset.
	Basically, this does the opposite of place_mark(): instead of 
	calculating the offset based off the x- and y-coordinate, the 
	coordinates are calculated based on the offset.
	'''
	return (offset % 3, offset / 3)

def find_wins(mark):
	'''
	Lists the winning coordinates to where the player can mark on their next 
	move! 'mark' is the character mark to look for.
	'''
	global wins
	global board
	win_coords = []
	for win_offsets in wins:
		num_marks = 0
		blank_offset = -1
		for i in win_offsets:
			if board.squares[i] == mark:
				num_marks += 1
			elif board.squares[i] is board.blank:
				blank_offset = i
		if num_marks == 2 and blank_offset >= 0:
			x, y = get_coords(blank_offset)
			win_coords.append([x, y])
	# no winning situations were found =\
	if len(win_coords) == 0:
		return None
	return win_coords

def find_fork(mark):
	'''
	Retrieves the first set of coordinates found to create a guaranteed 
	winning fork for the player marked with 'mark'.
	'''
	global board
	# STEP 1: find the offset of all spaces that can be marked
	blanks = board.blanks()
	# STEP 2: test each blank position to see if it is a fork :D
	memorize = board.squares[:]
	for offset in blanks:
		board.squares[offset] = mark
		# STEP 3: when placing the char mark on this area of the board, 
		# is it a fork? if so, return the offset's coordinates :D
		winning_coords = find_wins(mark)
		board.squares = memorize[:]
		if winning_coords != None and len(winning_coords) > 1:
			return get_coords(offset)
	# at this point we have found no forks =\
	return None

def setup_fork(mark):
	'''
	If we force the opponent to defend, can this move possibly setup a new
	fork? If so, return the coordinates of this fork trap. 
	'''
	global board
	# STEP 1: test each blank position to see if they force opponent to defend
	memorize = board.squares[:]
	opponent = 'O' if mark == 'X' else 'X'
	for offset in board.blanks():
		board.squares[offset] = mark
		winning_coord = find_wins(mark)
		if winning_coord:
			# STEP 2: if opponent will be forced to defend (due to an upcoming
			# win), mark that spot for the opponent.
			x, y = winning_coord[0]
			board.place(opponent, x, y)
			# STEP 4: does the force defend create an opportunities for a
			# fork setup? if this opportunity exists, then we found the 
			# coordinates to setup a fork!
			fork_coord = find_fork(mark)
			if fork_coord:
				# STEP 5: however, if opponent's forced move brings him into a 
				# position where we must block their win on the next turn, then 
				# disregard this offset as a good choice. (move onto next offset)
				block = find_wins(opponent)
				if block and block[0] != fork_coord:
					board.squares = memorize[:]
					continue
				
				# this is a genuine opportunity to setup a fork! return the 
				# coordinates of the mark's offset.
				board.squares = memorize[:]
				# return the coordinates for the successful fork setup offset!
				return get_coords(offset)
		# return the board to current state so we can test next offset.
		board.squares = memorize[:]
	return None

def computer_move(mark):
	'''
	Makes a move onto the game board for the computer. This is essentially 
	our Tic-Tac-Toe AI made for perfection.
	
	Parameter 'mark' is the computer's character mark (X or O)
	Returns a tuple of the computer's next movie's coordinates. 
	'''
	global board
	opponent = 'O' if mark == 'X' else 'X'
	
	# strategic priority:
	# 1 - go for winning move
	coord = find_wins(mark)
	if coord: return coord[0]
	# 2 - prevent human player's victory if we have to block
	coord = find_wins(opponent)
	if coord: return coord[0]
	# 3 - create a fork opportunity (to force a win!)
	coord = find_fork(mark)
	if coord: return coord
	
	# 4 - prevent human player from setting up a fork
	coord = find_fork(opponent)
	if coord:
		# since it is possible that the opponent could create another fork 
		# after 'coord' is marked by AI, this makes blocking 1 of 2 forks at 
		# 'coord' useless.
		memorize = board.squares[:]
		board.place(mark, coord[0], coord[1])
		if find_fork(opponent):
			# if there is another fork, block both forks by forcing the 
			# opponent to defend INSTEAD of creating an advantageous fork 
			# for themselves.
			#
			# STEP 1: find possible moves on the board (note: this will 
			# exclude the current 'coord', since this is a bad move anyways 
			# that allows the opponent to create another fork!)
			possibles = board.blanks()
			board.squares = memorize[:]
			# STEP 2: find a move that forces the opponent to defend. this 
			# forced defense MUST NOT create another fork!
			for i in possibles:
				board.squares[i] = mark
				force_coord = find_wins(mark)
				if find_wins(mark):
					fork_coord = find_fork(opponent)
					if force_coord != fork_coord:
						# awesome! we found a good offense to counter a fork!
						coord = get_coords(i)
						break
				# reset board and continue
				board.squares = memorize[:]
		# set the board back to normal, as if there were no pre-moves :)
		board.squares = memorize[:]
		return coord
	
	# 5 - if we can't fork right away, can we setup a fork?
	coord = setup_fork(mark)
	if coord: return coord
	
	# what are the strongest moves, respectively, when none of the 
	# above conditions are true? In situations where the computer 
	# does not go first, we'll have to consider these moves as well...
	
	# 6 - Grab the center (if available) -- YES, best defense if human
	#     gets the first move!!
	if opponent in board.squares and board.get(1, 1) is board.blank:
		return (1, 1)
		
	# 7 - Play in a corner (which one? adjacent corner? opposite corner?)
	if mark not in board.squares:
		corners = []
		ref = board.squares
		if ref[0] is board.blank: corners += [0]
		if ref[2] is board.blank: corners += [2]
		if ref[6] is board.blank: corners += [6]
		if ref[8] is board.blank: corners += [8]
		if len(corners) > 1: shuffle(corners)
		if len(corners) > 0: return get_coords(corners[0])

	# 8 - Mark one of the side squares (adjacent? opposite?) -- human 
	#     can force a winning fork if this is done before a corner is
	#     taken! better safe to play a corner before a side square
	# at this point in the AI, there will be no corner squares remaining,
	# so just play on the first available square remaining on the board.
	blanks = board.blanks()
	return get_coords(blanks[0])

def human_move(mark):
	'''
	Get the human player's move.
	'''
	global board
	coord = raw_input('What coordinates will you mark as "%s"? (ie: "0 2") ' % mark)
	x, y = coord.split()
	# make sure these values are proper integers
	try:
		x = int(x)
		y = int(y)
	except ValueError:
		print 'Your coordinates are off. Please only input 2 numbers separated by a space.'
		return human_move(mark)
	# hmm, we should also make sure these values are within range
	if x < 0 or x > 2 or y < 0 or y > 2:
		print 'Your coordinates are out of range. Valid ranges are from "0 0" to "2 2".'
		return human_move(mark)
	# is the space already occupied by another mark?
	if board.get(x, y) is not board.blank:
		print 'Cannot mark that space because it is already marked!'
		return human_move(mark)
	return (x, y)

def intro_game():
	'''Game introduction -- and any possible setup needed :)'''
	print '''
	Hi. I'm a computer. I'm going to demonstrate to you how AWESOME I am by 
	playing you a game of tic-tac-toe and never losing a single game!
	'''
	
	# STEP 1: initialize a new game
	global players
	global board
	players = {'X': '', 'O': ''}
	board = Board()
	# STEP 2: flip a coin to see which player goes first!
	if randint(0, 1):
		players['X'] = 'ai'
		players['O'] = 'human'
	else:
		players['X'] = 'human'
		players['O'] = 'ai'

def start_game():
	'''
	Starts the game and begins the main engine loop.
	'''
	global players
	global board
	turn = 'X'
	while board.winner() == None:
		if players[turn] == 'ai':
			coord = computer_move(turn)
		else:
			board.render()
			print 'Your Turn!'
			coord = human_move(turn)
		board.place(turn, coord[0], coord[1])
		# move to the next turn
		turn = 'O' if turn == 'X' else 'X'

def end_game():
	'''Displays the end-game results.'''
	global players
	global board
	board.render()
	winner = board.winner()
	if winner == 'T':
		print 'Not bad, so we tied.'
	elif players[winner] == 'ai':
		print 'See? I told you I was awesome.'
	else:
		print 'What?! Impossible! Robert needs to make me perfect.'

def proof():
	'''
	Tests if the computer's AI is perfect or not. If it is, then this will 
	give you proof that the computer AI will never lose!
	'''
	global board
	

# possible game modes:
#    'play' - play the game :)
#    'proof' - prove that the AI will never lose.
#    'watch' - watch a game history
#    any other mode will just play the game.
mode = ''
if mode == 'proof':
	print 'hai. yew in testing mode.'
	proof()
elif mode == 'watch':
	print 'nothing done yet.'
else:
	intro_game()
	start_game()
	end_game()
