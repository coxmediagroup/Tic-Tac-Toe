def get_best_move(board, player):
	""" 
	Returns the Best Move for the given Player. 
	
	Strategy based on this Wikipedia article: 
	http://en.wikipedia.org/wiki/Tic-tac-toe#Strategy
	"""

	""" Top Row Victories """

	# Top-Left and Top-Center are owned by Player. Top-Right is Open.
	if board.top_left == player 			\
		and board.top_center == player  	\
		and board.top_right == 0:
			return 'top_right'

	# Top-Left is Open. Top-Center and Top-Right are owned by Player.
	if board.top_left == 0					\
		and board.top_center == player  	\
		and board.top_right == player:
			return 'top_left'

	# Top-Left and Top-Right are owned by Player. Top-Center is Open.
	if board.top_left == player       		\
		and board.top_center == 0 			\
		and board.top_right == player:
			return 'top_center'

	""" Center Row Victories. """

	# Left and Center are Owned by Player. Right is Open.
	if board.left == player       			\
		and board.center == player 			\
		and board.right == 0:
			return 'right'

	# Left and Right are owned by Player. Center is Open.
	if board.left == player       			\
		and board.center == 0      			\
		and board.right == player:
			return 'center'

	# Left is Open. Center and Right are Owned by the Player.
	if board.left == 0             			\
		and board.center == player 			\
		and board.right == player:
			return 'left'

	""" Bottom Row Victories. """

	# Bottom Left and Bottom Center owned by Player. Bottom right is Open.
	if board.bottom_left == player 			\
		and board.bottom_center == player 	\
		and board.bottom_right == 0:
			return 'bottom_right'

	# Bottom Left and Bottom Right owned by Player. Bottom Center is Open.
	if board.bottom_left == player 			\
		and board.bottom_center == 0 		\
		and board.bottom_right == player:
			return 'bottom_center'

	# Bottom Left is Open. Bottom Center and Bottom Right owned by Player.
	if board.bottom_left == 0  				\
		and board.bottom_center == player 	\
		and board.bottom_right == player:
			return 'bottom_left'

	""" Left Column Victories """

	# Top-Left and Left owned by Player. Bottom-Left is Open.
	if board.top_left == player  			\
		and board.left == player 			\
		and board.bottom_left == 0:
			return 'bottom_left'

	# Top-Left and Bottom-Left owned by Player. Left is Open.
	if board.top_left == player  			\
		and board.left == 0	 				\
		and board.bottom_left == player:
			return 'left'

	# Left and Bottom-Left owned by Player. Top-Left is Open.
	if board.top_left == 0  		 		\
		and board.left == player 		 	\
		and board.bottom_left == player:
			return 'top_left'

	""" Center Column Victories """

	# Top-Center and Center owned by Player. Bottom-Center is Open.
	if board.top_center == player  			\
		and board.center == player 			\
		and board.bottom_center == 0:
			return 'bottom_center'

	# Center and Bottom-Center owned by Player. Top-Center is Open.
	if board.top_center == 0  		 		\
		and board.center == player	 		\
		and board.bottom_center == player:
			return 'top_center'

	# Top-Center and Bottom-Center owned by Player. Center is Open.
	if board.top_center == player  		 	\
		and board.center == 0 				\
		and board.bottom_center == player:
			return 'center'

	""" Right Column Victories """

	# Top-Right and Right owned by Player. Bottom-Right is Open.
	if board.top_right == player  			\
		and board.right == player 			\
		and board.bottom_right == 0:
			return 'bottom_right'

	# Top-Right and Bottom-Right owned by Player. Right is Open.
	if board.top_right == player  			\
		and board.right == 0	 			\
		and board.bottom_right == player:
			return 'right'

	# Right and Bottom-Right owned by Player. Top-Right is Open.
	if board.top_right == 0  		 	 	\
		and board.right == player 		 	\
		and board.bottom_right == player:
			return 'top_right'

	""" Diagonal Victories """

	# Top-Left, Center owned by Player. Bottom-Right is Open.
	if board.top_left == player 			\
		and board.center == player 		 	\
		and board.bottom_right == 0:
			return 'bottom_right'

	# Top-Left and Bottom-Right owned by Player. Center is Open.
	if board.top_left == player 			\
		and board.center == 0			 	\
		and board.bottom_right == player:
			return 'center'

	# Top-Left is Open. Center and Bottom-Right is owned by Player.
	if board.top_left == 0 					\
		and board.center == player 			\
		and board.bottom_right == player:
			return 'top_left'

	# Top-Right and Center owned by Player. Bottom-Left is Open.
	if board.top_right == player 			\
		and board.center == player 			\
		and board.bottom_left == 0:
			return 'bottom_left'

	# Top-Right and Bottom-Left are owned by Player. Center is Open.
	if board.top_right == player 			\
		and board.center == 0 				\
		and board.bottom_left == player:
			return 'center'

	# Top-Right is Open. Center and Bottom-Left are owned by Player.
	if board.top_right == 0 				\
		and board.center == player 			\
		and board.bottom_left == player:
			return 'top_right'

	""" Top Row Blocks """

	# Top-Left and Top-Center are owned by Player. Top-Right is Open.
	if board.top_left == -player 			\
		and board.top_center == -player  	\
		and board.top_right == 0:
			return 'top_right'

	# Top-Left is Open. Top-Center and Top-Right are owned by Player.
	if board.top_left == 0					\
		and board.top_center == -player  	\
		and board.top_right == -player:
			return 'top_left'

	# Top-Left and Top-Right are owned by Player. Top-Center is Open.
	if board.top_left == -player       		\
		and board.top_center == 0 			\
		and board.top_right == -player:
			return 'top_center'

	""" Center Row Blocks """

	# Left and Center are Owned by Player. Right is Open.
	if board.left == -player       			\
		and board.center == -player 			\
		and board.right == 0:
			return 'right'

	# Left and Right are owned by Player. Center is Open.
	if board.left == -player       			\
		and board.center == 0      			\
		and board.right == -player:
			return 'center'

	# Left is Open. Center and Right are Owned by the Player.
	if board.left == 0             			\
		and board.center == -player 			\
		and board.right == -player:
			return 'left'

	""" Bottom Row Blocks """

	# Bottom Left and Bottom Center owned by Player. Bottom right is Open.
	if board.bottom_left == -player 			\
		and board.bottom_center == -player 	\
		and board.bottom_right == 0:
			return 'bottom_right'

	# Bottom Left and Bottom Right owned by Player. Bottom Center is Open.
	if board.bottom_left == -player 			\
		and board.bottom_center == 0 		\
		and board.bottom_right == -player:
			return 'bottom_center'

	# Bottom Left is Open. Bottom Center and Bottom Right owned by Player.
	if board.bottom_left == 0  				\
		and board.bottom_center == -player 	\
		and board.bottom_right == -player:
			return 'bottom_left'

	""" Left Column Blocks """

	# Top-Left and Left owned by Player. Bottom-Left is Open.
	if board.top_left == -player  			\
		and board.left == -player 			\
		and board.bottom_left == 0:
			return 'bottom_left'

	# Top-Left and Bottom-Left owned by Player. Left is Open.
	if board.top_left == -player  			\
		and board.left == 0	 				\
		and board.bottom_left == -player:
			return 'left'

	# Left and Bottom-Left owned by Player. Top-Left is Open.
	if board.top_left == 0  		 		\
		and board.left == -player 		 	\
		and board.bottom_left == -player:
			return 'top_left'

	""" Center Column Blocks """

	# Top-Center and Center owned by Player. Bottom-Center is Open.
	if board.top_center == -player  			\
		and board.center == -player 			\
		and board.bottom_center == 0:
			return 'bottom_center'

	# Center and Bottom-Center owned by Player. Top-Center is Open.
	if board.top_center == 0  		 		\
		and board.center == -player	 		\
		and board.bottom_center == -player:
			return 'top_center'

	# Top-Center and Bottom-Center owned by Player. Center is Open.
	if board.top_center == -player  		 	\
		and board.center == 0 				\
		and board.bottom_center == -player:
			return 'center'

	""" Right Column Blocks """

	# Top-Right and Right owned by Player. Bottom-Right is Open.
	if board.top_right == -player  			\
		and board.right == -player 			\
		and board.bottom_right == 0:
			return 'bottom_right'

	# Top-Right and Bottom-Right owned by Player. Right is Open.
	if board.top_right == -player  			\
		and board.right == 0	 			\
		and board.bottom_right == -player:
			return 'right'

	# Right and Bottom-Right owned by Player. Top-Right is Open.
	if board.top_right == 0  		 	 	\
		and board.right == -player 		 	\
		and board.bottom_right == -player:
			return 'top_right'

	""" Diagonal Blocks """

	# Top-Left, Center owned by Player. Bottom-Right is Open.
	if board.top_left == -player 			\
		and board.center == -player 		 	\
		and board.bottom_right == 0:
			return 'bottom_right'

	# Top-Left and Bottom-Right owned by Player. Center is Open.
	if board.top_left == -player 			\
		and board.center == 0			 	\
		and board.bottom_right == -player:
			return 'center'

	# Top-Left is Open. Center and Bottom-Right is owned by Player.
	if board.top_left == 0 					\
		and board.center == -player 			\
		and board.bottom_right == -player:
			return 'top_left'

	# Top-Right and Center owned by Player. Bottom-Left is Open.
	if board.top_right == -player 			\
		and board.center == -player 			\
		and board.bottom_left == 0:
			return 'bottom_left'

	# Top-Right and Bottom-Left are owned by Player. Center is Open.
	if board.top_right == -player 			\
		and board.center == 0 				\
		and board.bottom_left == -player:
			return 'center'

	# Top-Right is Open. Center and Bottom-Left are owned by Player.
	if board.top_right == 0 				\
		and board.center == -player 			\
		and board.bottom_left == -player:
			return 'top_right'

	""" Select Center """
	if board.center == 0:
		return 'center'

	""" Select a Corner (Forking Opportunity) """
	
	if board.top_left == 0:
		return 'top_left'

	if board.top_right == 0:
		return 'top_right'

	if board.bottom_left == 0:
		return 'bottom_left'

	if board.bottom_right == 0:
		return 'bottom_right'
