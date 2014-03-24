#Class file for the tic-tac-toe board

class GameBoard(object):
	
	def __init__(self):
		self.board_data = ["1" , "2" , "3" , "4" , "5" , "6" , "7" , "8" , "9"]
		
	##board_data contains all the data that goes into the gameboard, it will contain numbers for spaces player can move to,
	##or spaces that contain a move (X or O).
	board_data = []	
	def draw_board(self):
		print "  |   | "
		print "%c | %c | %c " % (self.board_data[0] , self.board_data[1] , self.board_data[2])
		print "----------"
		print "%c | %c | %c " % (self.board_data[3] , self.board_data[4] , self.board_data[5])
		print "----------"
		print "%c | %c | %c " % (self.board_data[6] , self.board_data[7] , self.board_data[8])
		print "  |   | "
		
	##this function updates the board's data space is the selected space and player_token is either an X or O depening if 
	##the player or the computer made the move
	def update_board_data(self, space, player_token):
		self.board_data[space - 1 ] = player_token