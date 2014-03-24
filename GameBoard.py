#Class file for the tic-tac-toe board

class GameBoard(object):
	
	def __init__(self):
		self.board_data = ["1" , "2" , "3" , "4" , "5" , "6" , "7" , "8" , "9"]
		self.board_moves_left = ["1" , "2" , "3" , "4" , "5" , "6" , "7" , "8" , "9"] 
		
	##board_data contains all the data that goes into the gameboard, it will contain numbers for spaces player can move to,
	##or spaces that contain a move (X or O).
	board_data = []	
	##moves_left contains the board numbers that are left to play
	board_moves_left = []
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
		##need to correct the index since the user enters an index that is +1
		correctedIndex = int(space) - 1
		self.board_data[correctedIndex] = player_token
		self.board_moves_left.pop(correctedIndex)
	
	
	def get_board_data(self):
		return self.board_data
	def get_board_moves_left(self):
		return self.board_moves_left