# Tic Tac Toe
# -- classic game :)
from random import shuffle

board = ['-'] * 9

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


def winner(char = ''):
	'''
	Determines if someone won Tic Tac Toe :D
	Returns X if the X player won; O if O player won.
	'''
	global board
	
	if char == '':
		# if no character was specified, check if X won, then check if O won
		if winner('X'): return 'X'
		if winner('O'): return 'O'
	else:
		# did someone win horizontally?
		if board[0] == board[1] == board[2] == char:
			return char
		if board[3] == board[4] == board[5] == char:
			return char
		if board[6] == board[7] == board[8] == char:
			return char
	
		# can we find a vertical winner?
		if board[0] == board[3] == board[6] == char:
			return char
		if board[1] == board[4] == board[7] == char:
			return char
		if board[2] == board[5] == board[8] == char:
			return char
		
		# did a diagonal player win?
		if board[0] == board[4] == board[8] == char:
			return char
		if board[2] == board[4] == board[6] == char:
			return char
			
	# what if there was a tie? this is always possible. return 'T'.
	if '-' not in board: return 'T'
	
	return None


def find_wins(char):
	'''
	Lists the winning coordinates to where the player can mark on their next 
	move! 'char' is the character mark to look for.
	'''
	win_coords = []
	# STEP 1: search for horizontal wins
	for y in range(3):
		marks = []
		blank = []
		for x in range(3):
			if get_mark(x, y) == char:
				marks.append([x, y])
			elif get_mark(x, y) == '-':
				blank.append([x, y])
		# if there were 2 character marks and 1 blank mark, then there's a
		# winning opportunity!
		if len(marks) == 2 and len(blank) == 1:
			win_coords.append(blank)
	# STEP 2: search for vertical wins
	for x in range(3):
		marks = []
		blank = []
		for y in range(3):
			if get_mark(x, y) == char:
				marks.append([x, y])
			elif get_mark(x, y) == '-':
				blank.append([x, y])
		if len(marks) == 2 and len(blank) == 1:
			win_coords.append(blank)
	# STEP 3: search the game board's 2 diagonals for a win
	global board
	num_marks = 0
	blank = []
	diag_offsets = (0, 4, 8)
	for i in diag_offsets:
		if board[i] == char:
			num_marks += 1
		elif board[i] == '-':
			blank.append(get_coords(i))
	if num_marks == 2 and len(blank) == 1:
		win_coords.append(blank)
	# test the next diagonal
	num_marks = 0
	blank = []
	diag_offsets = (2, 4, 6)
	for i in diag_offsets:
		if board[i] == char:
			num_marks += 1
		elif board[i] == '-':
			blank.append(get_coords(i))
	if num_marks == 2 and len(blank) == 1:
		win_coords.append(blank)
	# no winning situations were found :(
	if len(win_coords) == 0:
		return None
	return win_coords

def ai_take_win():
	'''
	Returns the coordinates to win the tic-tac-toe match!
	False if the computer's AI can not win.
	'''
	global board
	# Step 1: 
	# find the pattern where there are 2 X's in a row followed by open area
	# pattern = ('X', 'X', '-')
	# VERTICAL PATTERNS
	# for col in range(3):
	# for row in range(3):
	# 	# computer's marks on the board, and our blank square coordinates
	# 	marks = []
	# 	blank = ()
		
	return False

def ai_block_win():
	'''
	Returns the coordinates to block the opponents win.
	False if opponent cannot win.
	'''
	# Step 1: 
	# find the pattern where there are 2 X's in a row followed by open area
	
	return False

def ai_take_fork():
	'''
	Returns coordinates to setup a fork to guarantee the next move is a win!
	Returns False if there are no fork opportunities.
	'''
	
	return False

def ai_block_fork():
	'''
	Returns the coordinates to blocks an opponents fork opportunity.
	False if the opponent has no chance. 
	'''

def computer_move():
	'''
	Makes a move onto the game board for the computer. This is essentially 
	our Tic-Tac-Toe AI made for perfection.
	
	Returns a tuple of the computer's next movie's coordinates. 
	'''
	global board
	
	# beginning game strategy: play a corner, because this gives human players
	# less squares to force a tie :)
	if 'X' not in board:
		corners = [0, 2, 6, 8]
		shuffle(corners)
		return get_coords(corners[0])
	else:	
		global memorize
		try:
			memorize
		except:
			# memorize the player board and find the opponent's first move
			memorize = board[:]
			coord = get_coords(memorize.index('O'))
			# print 'first move is: ', coord
		
		# strategic priority:
		# 1 - go for winning move
		if ai_take_win(): return ai_take_win()
		# 2 - prevent human player's victory if we have to block
		if ai_block_win(): return ai_block_win()
		# 3 - create a fork opportunity (to force a win!)
		if ai_take_fork(): return ai_take_fork()
		# 4 - prevent human player from setting up a fork
		if ai_block_fork(): return ai_block_fork()
		
		# what are the strongest moves, respectively, when none of the 
		# above conditions are true? In situations where the computer 
		# does not go first, we'll have to consider those moves as well.
		
		# ? - Grab the center (if available)
		# ? - Mark one of the side squares (adjacent? opposite?)
		# ? - Play in a corner (which one? adjacent corner? opposite corner?)
		
		# for now: simple AI that just adds a mark on the board
		for offset in range(len(board)):
			# if this is an open mark on the tic-tac-toe bard, release its coordinates!
			if board[offset] == '-':
				return get_coords(offset)

def human_move():
	'''
	Get the human player's move.
	'''
	coord = raw_input('What are the coordinates of your move? (ie: "0 2") ')
	x, y = coord.split()
	# make sure these values are proper integers
	try:
		# hmm, we should also make sure these values are within range
		return (int(x), int(y))
	except ValueError:
		print 'Your coordinates are off. Please only input 2 numbers separated by a space.'
		return human_move()

def intro_game():
	'''Game introduction -- and any possible setup needed :)'''
	print '''
		Hi. I'm a computer. I'm going to demonstrate to you how AWESOME I am by 
		playing you a game of tic-tac-toe and never losing a single game! I'll 
		make the first move though.
	'''

def start_game():
	'''
	Starts the game and begins the main engine loop.
	'''
	while winner() == None:
		coord = computer_move()
		place_mark('X', coord[0], coord[1])
		render_board()
		# break loop if the computer had the winning move (or tie)
		if winner('X') or winner('T'):
			break
		print 'Your Move!'
		coord = human_move()
		place_mark('O', coord[0], coord[1])

def end_game():
	# end game
	render_board()
	if winner() == 'X':
		print 'See? I told you I was awesome.'
	elif winner() == 'O':
		print 'What?! Impossible! Robert needs to make me perfect.'
	else:
		print 'Not bad, so we tied.'

# intro_game()
# start_game()
# end_game()