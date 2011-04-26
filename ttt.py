# Tic Tac Toe
# -- classic game :)

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


def winner(char = ''):
	'''
	Determines if someone won Tic Tac Toe :D
	Returns X if the X player won; O if O player won.
	'''
	global board
	
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
	
	return None

def computer_move():
	'''
	Makes a move onto the game board for the computer. This is essentially 
	our Tic-Tac-Toe AI.
	
	Returns a tuple of the computer's next movie's coordinates. 
	'''
	global board
	# for now: simple AI that just adds a mark on the board
	for offset in range(len(board)):
		# if this is an open mark on the tic-tac-toe bard, release its coordinates!
		if board[offset] == '-':
			return (offset % 3, offset / 3)
			
	# return (1, 1)

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
	print 'Your Move!'
	coord = human_move()
	place_mark('O', coord[0], coord[1])
