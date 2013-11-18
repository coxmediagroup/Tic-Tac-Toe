def get_opening(triple, player=None):
	"""
	Checks the three game pieces to determine if the Player can make a move to
	have three-in-a-row.
	"""
	if triple[0][1] == triple[1][1] == player and triple[2][1] == 0:
		return triple[2][0]
	if triple[0][1] == triple[2][1] == player and triple[1][1] == 0:
		return triple[1][0]
	if triple[1][1] == triple[2][1] == player and triple[0][1] == 0:
		return triple[0][0]

def get_best_move(board, player):
	""" 
	Returns the Best Move for the given Player. 
	
	Strategy based on this Wikipedia article: 
	http://en.wikipedia.org/wiki/Tic-tac-toe#Strategy
	"""
	# Collect Move-Combinations a Data-Structure for Programmatic iterations.
	triples = [

		# Rows
		[ 
			( 'top_left', board.top_left ), 
			( 'top_right', board.top_right ), 
			( 'top_center', board.top_center )
		],
		[ 
			( 'left', board.left ), 
			( 'center', board.center ), 
			( 'right', board.right )
		],
		[ 
			( 'bottom_left', board.bottom_left ),
			( 'bottom_center', board.bottom_center ),
			( 'bottom_right', board.bottom_right )
		],

		# Columns
		[ 
			( 'top_left', board.top_left ),
			( 'left', board.left ), 
			( 'bottom_left', board.bottom_left ) 
		],
		[ 
			( 'top_center', board.top_center ), 
			( 'center', board.center ), 
			( 'bottom_center', board.bottom_center )
		],
		[ 
			( 'top_right', board.top_right ), 
			( 'right', board.right ), 
			( 'bottom_right', board.bottom_right )
		],

		# Diaganols
		[ 
			( 'top_left', board.top_left ), 
			( 'center', board.center ), 
			( 'bottom_right', board.bottom_right )
		],
		[ 
			( 'bottom_left', board.bottom_left ), 
			( 'center', board.center ), 
			( 'top_right', board.top_right ) 
		]

	]

	# Victories
	for triple in triples:
		victory = get_opening(triple, player)
		if victory:
			return victory

	# Blocks
	for triple in triples:
		block = get_opening(triple, -player)
		if block:
			return block

	# @TODO To Enhance the Computer's Ability to win against Human Opponents,
	# the processes of 'Fork' and 'Blocking an Opponent's Fork' should be
	# implemented here.

	# Select the Center
	if board.center == 0: return 'center'

	# Opposite Corners
	if board.top_left == -player and board.bottom_right == 0: 
		return 'bottom_right'
	if board.top_right == -player and board.bottom_left == 0: 
		return 'bottom_left'
	if board.top_left == 0 and board.bottom_right == -player: 
		return 'top_left'
	if board.top_right == 0 and board.bottom_left == -player: 
		return 'top_right'

	# Select an Empty Corner
	if board.top_left == 0: return 'top_left'
	if board.top_right == 0: return 'top_right'
	if board.bottom_left == 0: return 'bottom_left'
	if board.bottom_right == 0: return 'bottom_right'

	# Select an Empty Side
	if board.top_center == 0: return 'top_center'
	if board.left == 0: return 'left'
	if board.right == 0: return 'right'
	if board.bottom_center == 0: return 'bottom_center'

