#Class file for the tic-tac-toe board

class GameBoard(object):
	
	def __init__(self):
		self.board_data = ["1" , "2" , "3" , "4" , "5" , "6" , "7" , "8" , "9"]
		
	##board_data contains all the data that goes into the gameboard, it will contain numbers for spaces player can move to,
	##or spaces that contain a move (X or O).
	board_data = []	
	
	##This dictionary contains all 8 possible way to win the game
	##1 and 2 are the horizontal wins
	##3-6 are vertical wins
	##6-8 are horizontal wins
	board_winning_paths = {
		1:[0 , 4 , 8] , 2:[2 , 4 , 6] , 3:[0 , 3 , 6] , 4:[1 , 4 , 7] ,
		5:[2 , 5 , 8] , 6:[0 , 1 , 2] , 7:[3 , 4 , 5] , 8:[6 , 7 , 8]
	}
		
	def draw_board(self):

		print "  |   | "
		print "%c | %c | %c " % (self.board_data[0] , self.board_data[1] , self.board_data[2])
		print "----------"
		print "%c | %c | %c " % (self.board_data[3] , self.board_data[4] , self.board_data[5])
		print "----------"
		print "%c | %c | %c " % (self.board_data[6] , self.board_data[7] , self.board_data[8])
		print "  |   | "
		
	##this function updates the board's data space is the selected space and player_token is either an X or O depending if 
	##the player or the computer made the move
	def update_board_data(self , space , player_token):
		self.board_data[int(space) - 1] = player_token
	
	def get_board_data(self):
		return self.board_data
	def get_board_moves_left(self):
		moves_left = []
		for items in self.board_data:
			if items != "X" or items != "O":
				moves_left.append(items)
		return moves_left
	def count_board_moves_left(self):
		return len(self.get_board_moves_left())
		
	##check all paths to see if the game has a winner
	def check_for_winner(self):
	
		##loop through the dictionary
		for key, value in self.board_winning_paths.iteritems():
			##player_token_count keeps track of how many player tokens we have in a row
			player_token_count = 0
			##cpu_token_count keeps track of how many computer tokens we have in a row
			cpu_token_count = 0
			##nested loop for the board positions that result in a win
			for board_positions in value:
					##if the value is not an X or O stop the loop since its not possible to win
					if (board_positions != "X" or board_positions != "O"):
						break
					elif (board_positions == "X"):
						player_token_count += 1
					else:
						cpu_token_count += 1
			if(player_token_count == 3):
				return "player wins"
			elif(cpu_token_count == 3):
				return "computer wins"
		##if no winner return false after we check every possible way to win
		return False
		