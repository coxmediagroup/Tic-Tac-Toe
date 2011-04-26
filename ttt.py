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


def coords(offset):
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
		return coords(corners[0])
	else:	
		# for now: simple AI that just adds a mark on the board
		for offset in range(len(board)):
			# if this is an open mark on the tic-tac-toe bard, release its coordinates!
			if board[offset] == '-':
				return coords(offset)

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


# introduction
print '''
	Hi. I'm a computer. I'm going to demonstrate to you how AWESOME I am by 
	playing you a game of tic-tac-toe and never losing a single game! I'll 
	make the first move though. Press the enter/return key when you are ready 
	for a beating!
'''

# main game loop
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

# end game
render_board()
if winner() == 'X':
	print 'See? I told you I was awesome.'
elif winner() == 'O':
	print 'What?! Impossible! Robert needs to make me perfect.'
else:
	print 'Not bad, so we tied.'
