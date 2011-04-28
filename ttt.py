# Tic Tac Toe
# -- classic game :)
from random import shuffle, randint

def render_board():
	'''
	Renders the Tic Tac Toe game board to the screen.
	'''
	global board
	print board[0], board[1], board[2]
	print board[3], board[4], board[5]
	print board[6], board[7], board[8]


def place_mark(mark, x, y):
	'''
	Place a mark on the game board. minimum to maximum coordinates range from 
	(0, 0) to (2, 2)
	'''
	global board
	offset = y * 3 + x
	board[offset] = mark[0]


def get_mark(x, y):
	'''
	Returns the mark at (x, y) on our game board. If (x, y) is out of range 
	then return None.
	'''
	global board
	if x < 0 or x > 2 or y < 0 or y > 2:
		return None
	return board[y * 3 + x]


def get_coords(offset):
	'''
	Returns a tuple pair of coordinates based on the game board's offset.
	Basically, this does the opposite of place_mark(): instead of 
	calculating the offset based off the x- and y-coordinate, the 
	coordinates are calculated based on the offset.
	'''
	return (offset % 3, offset / 3)


def winner(mark = ''):
	'''
	Determines if someone won Tic Tac Toe :D
	Returns X if the X player won; O if O player won.
	'''
	global board
	
	# what if there was a tie? this is always possible. return 'T'.
	if '-' not in board: return 'T'
	
	if mark == '':
		# if no mark was specified, check if X won, then check if O won
		if winner('X') == 'X': return 'X'
		if winner('O') == 'O': return 'O'
	else:
		# did someone win horizontally?
		if board[0] == board[1] == board[2] == mark:
			return mark
		if board[3] == board[4] == board[5] == mark:
			return mark
		if board[6] == board[7] == board[8] == mark:
			return mark
		
		# can we find a vertical winner?
		if board[0] == board[3] == board[6] == mark:
			return mark
		if board[1] == board[4] == board[7] == mark:
			return mark
		if board[2] == board[5] == board[8] == mark:
			return mark
		
		# did a diagonal player win?
		if board[0] == board[4] == board[8] == mark:
			return mark
		if board[2] == board[4] == board[6] == mark:
			return mark
		
	return None


def find_blanks():
	'''Returns a list of all offset positions that can take a new mark.'''
	global board
	blanks = []
	for i in range(len(board)):
		if board[i] == '-':
			blanks.append(i)
	return blanks

def find_wins(mark):
	'''
	Lists the winning coordinates to where the player can mark on their next 
	move! 'mark' is the character mark to look for.
	'''
	win_coords = []
	# STEP 1: search for horizontal wins
	for y in range(3):
		marks = []
		blank = []
		for x in range(3):
			if get_mark(x, y) == mark:
				marks.append([x, y])
			elif get_mark(x, y) == '-':
				blank.append([x, y])
		# if there were 2 character marks and 1 blank mark, then there's a
		# winning opportunity!
		if len(marks) == 2 and len(blank) == 1:
			win_coords.append(blank[0])
	# STEP 2: search for vertical wins
	for x in range(3):
		marks = []
		blank = []
		for y in range(3):
			if get_mark(x, y) == mark:
				marks.append([x, y])
			elif get_mark(x, y) == '-':
				blank.append([x, y])
		if len(marks) == 2 and len(blank) == 1:
			win_coords.append(blank[0])
	# STEP 3: search the game board's 2 diagonals for a win
	global board
	# each diagonal includes a tuple set of diagonal offsets
	diagonals = ((0, 4, 8), (2, 4, 6))
	for diag_offsets in diagonals:
		num_marks = 0
		# blank = -1
		found_blank = False
		# diag_offsets = (0, 4, 8)
		for i in diag_offsets:
			if board[i] == mark:
				num_marks += 1
			elif board[i] == '-':
				# blank = i
				found_blank = True
		# if num_marks == 2 and blank >= 0:
		if num_marks == 2 and found_blank:
			x, y = get_coords(found_blank)
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
	blanks = []
	for i in range(len(board)):
		if board[i] == '-':
			blanks.append(i)
	# STEP 2: test each blank position to see if it is a fork :D
	memorize = board[:]
	for offset in blanks:
		board[offset] = mark
		# STEP 3: when placing the char mark on this area of the board, 
		# is it a fork? if so, return the offset's coordinates :D
		winning_coords = find_wins(mark)
		board = memorize[:]
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
	# blanks = find_blanks()
	memorize = board[:]
	opponent = 'O' if mark == 'X' else 'X'
	for offset in find_blanks():
		board[offset] = mark
		winning_coord = find_wins(mark)
		if winning_coord:
			# STEP 2: if opponent will be forced to defend (due to an upcoming
			# win), mark that spot for the opponent.
			x, y = winning_coord[0]
			place_mark(opponent, x, y)
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
					board = memorize[:]
					continue
				
				# this is a genuine opportunity to setup a fork! return the 
				# coordinates of the mark's offset.
				board = memorize[:]
				# return the coordinates for the successful fork setup offset!
				return get_coords(offset)
		# return the board to current state so we can test next offset.
		board = memorize[:]
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
		memorize = board[:]
		place_mark(mark, coord[0], coord[1])
		if find_fork(opponent):
			# if there is another fork, block both forks by forcing the 
			# opponent to defend INSTEAD of creating an advantageous fork 
			# for themselves.
			#
			# STEP 1: find possible moves on the board (note: this will 
			# exclude the current 'coord', since this is a bad move anyways 
			# that allows the opponent to create another fork!)
			possibles = find_blanks()
			board = memorize[:]
			# STEP 2: find a move that forces the opponent to defend. this 
			# forced defense MUST NOT create another fork!
			for i in possibles:
				board[i] = mark
				force_coord = find_wins(mark)
				if find_wins(mark):
					fork_coord = find_fork(opponent)
					if force_coord != fork_coord:
						# awesome! we found a good offense to counter a fork!
						coord = get_coords(i)
						break
				# reset board and continue
				board = memorize[:]
		# set the board back to normal, as if there were no pre-moves :)
		board = memorize[:]
		return coord
	
	# 5 - if we can't fork right away, can we setup a fork?
	coord = setup_fork(mark)
	if coord: return coord
	
	# what are the strongest moves, respectively, when none of the 
	# above conditions are true? In situations where the computer 
	# does not go first, we'll have to consider these moves as well...
	
	# 6 - Grab the center (if available) -- YES, best defense if human
	#     gets the first move!!
	if opponent in board and get_mark(1, 1) == '-':
		return (1, 1)
		
	# 7 - Play in a corner (which one? adjacent corner? opposite corner?)
	if mark not in board:
		corners = []
		if board[0] == '-': corners += [0]
		if board[2] == '-': corners += [2]
		if board[6] == '-': corners += [6]
		if board[8] == '-': corners += [8]
		if len(corners) > 1: shuffle(corners)
		if len(corners) > 0: return get_coords(corners[0])

	# 8 - Mark one of the side squares (adjacent? opposite?) -- human 
	#     can force a winning fork if this is done before a corner is
	#     taken! better safe to play a corner before a side square
	# at this point in the AI, there will be no corner squares remaining,
	# so just select whatever space is remaining.
	for offset in range(len(board)):
		# if this is an open mark on the tic-tac-toe bard, release its coordinates!
		if board[offset] == '-':
			return get_coords(offset)
	return None

def human_move():
	'''
	Get the human player's move.
	'''
	coord = raw_input('What are the coordinates of your move? (ie: "0 2") ')
	x, y = coord.split()
	# make sure these values are proper integers
	try:
		x = int(x)
		y = int(y)
	except ValueError:
		print 'Your coordinates are off. Please only input 2 numbers separated by a space.'
		return human_move()
	# hmm, we should also make sure these values are within range
	if x < 0 or x > 2 or y < 0 or y > 2:
		print 'Your coordinates are out of range. Valid ranges are from "0 0" to "2 2".'
		return human_move()
	# is the space already occupied by another mark?
	if get_mark(x, y) != '-':
		print 'Cannot mark that space because it is already marked!'
		return human_move()
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
	board = ['-'] * 9
	
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
	turn = 'X'
	while winner() == None:
		if players[turn] == 'ai':
			coord = computer_move(turn)
		else:
			render_board()
			print 'Your Turn!'
			coord = human_move()
		place_mark(turn, coord[0], coord[1])
		# move to the next turn
		turn = 'O' if turn == 'X' else 'X'

def end_game():
	'''Displays the end-game results.'''
	global players
	render_board()
	if winner() == 'T':
		print 'Not bad, so we tied.'
	elif players[winner()] == 'ai':
		print 'See? I told you I was awesome.'
	else:
		print 'What?! Impossible! Robert needs to make me perfect.'

intro_game()
start_game()
end_game()