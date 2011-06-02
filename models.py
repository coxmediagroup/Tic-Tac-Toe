import re, random

human = '1' #X
computer = '2' #O
				
class Board:
	# this model represent the board when the request is handled. 
	# I avoided using db models because that would have been too much overhead for too little gain
	
	
	def __init__(self, board_state):
		self.board_state = board_state #9 digit base 3 string 0 = empty, 1 = X, 2 = O
		
	def update_state(self, index, symbol):
		# update the board state when a move is made.
		index = int(index)
		state_list = list(self.board_state)
		state_list[index] = symbol
		self.board_state = ''.join(state_list)
	
					
	def execute_move(self, move, symbol):
		self.update_state(move, symbol)
		
	def reverse_move(self, move):
		return self.execute_move(move, '0')
		
	def game_over(self):
		return self.winner() or (self.get_valid_moves() == [])
			
	def all_equal(self, line):
		#determine if all the symbols in a line are equal
		if not line:
			return False
		i = iter(line)
		first = i.next()
		for item in i:
			if first != item:
				return False
		return True
		
	def get_block_values(self, indeces):
		# gets the current board values for a list of indeces that are passed in
		return [self.board_state[index] for index in indeces]
	
	def winner(self):
		# detect any winning lines/columns/rows on the board
		win_lines = [[0,1,2],[3,4,5],[6,7,8],
					[0,3,6],[1,4,7],[2,5,8], # all line indeces on the board
					[0,4,8],[2,4,6]]
		
		for line in win_lines:
			if self.board_state[line[0]] != '0' and self.all_equal(self.get_block_values(line)):
				return self.board_state[line[0]]
		
	def get_valid_moves(self):
		#gete all the indeces on the board that haven't been filled
		empty_indeces = [match.start() for match in re.finditer(re.escape('0'), self.board_state)]
		return empty_indeces
		
