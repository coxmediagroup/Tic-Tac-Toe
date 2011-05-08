# Tic Tac Toe
# -- classic game :)
import sys
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
	# a string of play history. each character is the numeric offset of where
	# the player placed their mark. 'X' always comes first.
	history = ''
	
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
		self.history += str(offset)
		
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
		
	def winner(self):
		'''
		Determines if someone won Tic Tac Toe :D
		Returns 'X' if the X player won; 'O' if O player won.
		Returns 'T' if there was a tie
		'''
		marks = ['X', 'O']
		for mark in marks:
			ref = self.squares
			global wins
			for win_offsets in wins:
				num_marks = 0
				for i in win_offsets:
					if board.squares[i] == mark:
						num_marks += 1
				if num_marks == 3:
					return mark
		# if no winning marks were found, test for a tie
		if self.blank not in self.squares:
			return 'T'
		else:
			return None
	def generate(self, history):
		'''
		Sets up a board based on the board history. Note: in this game of Tic
		Tac Toe, 'X' will always go first!
		'''
		turn = 'X'
		self.history = ''
		self.squares = [self.blank] * 9
		for offset in history:
			self.squares[int(offset)] = turn
			self.history += offset
			turn = 'O' if turn == 'X' else 'X'


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
	init_state = board.history
	for offset in blanks:
		board.squares[offset] = mark
		# STEP 3: when placing the char mark on this area of the board, 
		# is it a fork? if so, return the offset's coordinates :D
		winning_coords = find_wins(mark)
		board.generate(init_state)
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
	init_state = board.history
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
					board.generate(init_state)
					continue
				
				# this is a genuine opportunity to setup a fork! return the 
				# coordinates of the mark's offset.
				board.generate(init_state)
				# return the coordinates for the successful fork setup offset!
				return get_coords(offset)
		# return the board to current state so we can test next offset.
		board.generate(init_state)
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
		
	# 4 - prevent human player from setting up a fork--this only needs to be 
	# at a stage where at least 6 moves are remaining in the game.
	coord = find_fork(opponent)
	if coord and len(board.blanks()) <= 6:
		init_state = board.history
		board.place(mark, coord[0], coord[1])
		board.generate(init_state)
		# STEP 2: find a move that forces the opponent to defend. this 
		# forced defense MUST NOT create another fork for the opponent!
		for i in board.blanks():
			board.squares[i] = mark
			force_coord = find_wins(mark)
			if force_coord:
				# this forced defense MUST NOT allow opponent to fork on defense
				force_coord = tuple(force_coord[0])
				fork_coord = find_fork(opponent)
				if force_coord != fork_coord:
					# awesome! we found a good offense to counter a fork!
					coord = get_coords(i)
					break
			# reset board and continue
			board.generate(init_state)
		return coord
		
	# 5 - if we can't fork right away, can we setup a fork? this check is 
	# only useful after each player has made their first mark.
	if len(board.blanks()) < 7:
		coord = setup_fork(mark)
		if coord: return coord
		
	# what are the strongest moves, respectively, when none of the 
	# above conditions are true? In situations where the computer 
	# does not go first, we'll have to consider these moves as well...
	
	# 6 - Grab the center (if available) -- YES, best defense if human
	#     gets the first move!!
	if opponent in board.squares and board.get(1, 1) is board.blank:
		return (1, 1)
		
	# 7 - Play in a corner if there are more than 5 blanks available.
	if len(board.blanks()) > 5:
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


def do_proof():
	'''
	Tests if the computer's AI is perfect or not. If it is, then this will 
	give you proof that the computer AI will never lose!
	'''
	# Proof data
	game_outcomes = {'': None}
	random_threshold = 10
	plays_exhausted = False
	# STEP 1: setup game environment
	global players
	global board
	board = Board()
	players = {'X': '', 'O': ''}
	# STEP 2: will the computer go first in this proof?
	choice = 'x'
	while choice.lower()[0] != 'y' and choice.lower()[0] != 'n':
		choice = raw_input('will the computer go first? yes/no: ')
		
	if choice.lower()[0] == 'y':
		players['X'] = 'ai'
		players['O'] = 'human'
	else:
		players['X'] = 'human'
		players['O'] = 'ai'
		
	# STEP 3:
	# loop until all game outcomes have been exhausted
	# new_history stores dictionary keys for game_outcomes where the game is 
	# incomplete (has a value of None)
	new_history = ['']
	depth = 0
	while len(new_history) > 0:
		for turn in players:
			for game_history in new_history:
				# PART 1:
				# play the game history to create a game board in a playable state
				board.generate(game_history)
				
				# PART 2:
				# for each response in the game_outcomes where there is no winner, tie,
				# or flag to indicate that the history item has been exhausted, find ALL
				# possible computer AI responses.
				# for history in game_outcomes:
				if players[turn] == 'ai':
					# PART 3:
					# Find the AI algorithm's official move.
					#
					# While the AI algorithm may choose the same move every time, it is 
					# also possible that the algorithm will randomly select one of many 
					# coordinates.
					coords = []
					for i in range(random_threshold):
						move = computer_move(turn)
						if move not in coords:
							coords.append(move)
					# in the case where there are more than 1 unique set of coordinates, 
					# perform a more vigorous test to determine all possible moves.
					if len(coords) > 1:
						coords = []
						for i in range(random_threshold * 9):
							move = computer_move(turn)
							if move not in coords:
								coords.append(move)
					offsets = [y*3+x for x, y in coords]
				else:
					# it is the human's turn! since the human is free to select any 
					# blank space on the tic tac toe board, consider every blank space
					# as a possible play against the computer AI!
					offsets = board.blanks()
		
				# PART 4:
				# save the game history and outcome. The game history will be a string 
				# of offsets
				for offset in offsets:
					x, y = get_coords(offset)
					board.place(turn, x, y)
					game_outcomes[board.history] = board.winner()
					# reset game history on the board
					board.generate(game_history)
		
				# PART 5:
				# finally, since we exhausted all playable possibilities for this 
				# game state, mark this game history state as exhausted.
				# Exhaustion will be notated with an 'E'
				game_outcomes[game_history] = 'E'
			if '' in game_outcomes: del(game_outcomes[''])
			# grab the next available (and unplayed) history for the next player
			new_history = [key for key in game_outcomes if game_outcomes[key] is None]
			if len(new_history) == 0:
				break;
		depth += 1
		print 'History Depth Level has reached %d ...' % depth
		
	print
	print '========================================='
	print '   Results when %s begins the game:' % players['X']
	print '========================================='
	print
	print 'Total game positions: ', len(game_outcomes)
	exhausted = [k for k in game_outcomes if game_outcomes[k] is 'E']
	print 'exhausted move sets: ', len(exhausted)
	ties = [k for k in game_outcomes if game_outcomes[k] is 'T']
	print 'Ties: ', len(ties)
	x_wins = [k for k in game_outcomes if game_outcomes[k] is 'X']
	print 'X wins: ', len(x_wins)
	o_wins = [k for k in game_outcomes if game_outcomes[k] is 'O']
	print 'O wins: ', len(o_wins)
	none = [k for k in game_outcomes if game_outcomes[k] is None]
	print 'Still need exhaustion: ', len(none)
	print
	print '======================================'
	print ' Game Outcomes - where the human won!'
	print '======================================'
	print
	key_count = 0
	human_mark = 'O' if players['X'] == 'ai' else 'X'
	human_wins = [k for k in game_outcomes if game_outcomes[k] is human_mark]
	for key in human_wins:
		key_count += 1
		print str(key_count) + ':', 'history:', key, ' -  outcome:', game_outcomes[key]
	if len(human_wins) == 0:
		print 'Well it looks like the human NEVER won :)'
		print


# possible game modes:
#    'play' - play the game :)
#    'proof' - prove that the AI will never lose.
#    'watch' - watch a game history
#    any other mode will just play the game.
mode = sys.argv[1] if len(sys.argv) > 1 else ''
if mode != 'proof' and mode != 'watch': mode = ''

# board = Board()
if mode == 'proof':
	do_proof()
elif mode == 'watch':
	history = raw_input('input the game history to analyze: ')
	board = Board()
	turn = 'X'
	for move_offset in history:
		# print 'move_offset =', move_offset
		x, y = get_coords(int(move_offset))
		board.place(turn, x, y)
		board.render()
		turn = 'O' if turn == 'X' else 'X'
		raw_input('hit ENTER to continue...')
	print board.winner(), 'won!'
else:
	intro_game()
	start_game()
	end_game()
