from django.shortcuts import render_to_response

def game(request):
	return render_to_response('board.html')

def turn(board, player):
	opponent = {computer:human, human:computer}
		
	def judge(winner):
	"""judge whether or not the player has won the match"""
		if not winner:
			return 0
		if winner == player:
			return +1
		return -1
		
		
	def evaluate_move(move, p=player):
	"""evaluate the outcome of a particular move"""
		try:
			board.execute_move(move, p)
			if board.game_over():
				return judge(board.winner())
			valid_moves = board.get_valid_moves()
			
			outcomes = (evaluate_move(next_move, opponent[p]) for next_move in valid_moves)
			if p == player:
				min_element = 1
				for o in outcomes:
					if o == -1:
						return o
					min_element = min(o,min_element)
				return min_element
			else:
				max_element = -1
				for o in outcomes:
					if o == +1:
						return o
					max_element = max(o,max_element)
				return max_element
			
		finally:
			board.reverse_move(move)
			
	moves = [(move, evaluate_move(move)) for move in board.get_valid_moves()]
	random.shuffle(moves)
	moves.sort(key = lambda (move, winner): winner)
	import ipdb; ipdb.set_trace()