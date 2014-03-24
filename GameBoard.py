#Class file for the tic-tac-toe board
import random

class GameBoard(object):
	
	def __init__(self):
		self.board_data = ["1" , "2" , "3" , "4" , "5" , "6" , "7" , "8" , "9"]
		
	##board_data contains all the data that goes into the gameboard, it will contain numbers for spaces player can move to,
	##or spaces that contain a move (X or O).
	board_data = []	
	
	##The following data is used to help the computer know whats open and make the right decision
	corners = [0 , 2 , 6 , 8]
	sides = [1 , 3 , 5 , 7]
	
	##This dictionary contains all 8 possible way to win the game
	##1 and 2 are the horizontal wins
	##3-6 are vertical wins
	##6-8 are horizontal wins
	board_winning_paths = {
		1:[0 , 4 , 8] , 2:[2 , 4 , 6] , 3:[0 , 3 , 6] , 4:[1 , 4 , 7] ,
		5:[2 , 5 , 8] , 6:[0 , 1 , 2] , 7:[3 , 4 , 5] , 8:[6 , 7 , 8]
	}
		
	def draw_board(self):

		print "\n"
		print "  |   | "
		print "%c | %c | %c " % (self.board_data[0] , self.board_data[1] , self.board_data[2])
		print "----------"
		print "%c | %c | %c " % (self.board_data[3] , self.board_data[4] , self.board_data[5])
		print "----------"
		print "%c | %c | %c " % (self.board_data[6] , self.board_data[7] , self.board_data[8])
		print "  |   | "
		print " \n "
		
	##this function updates the board's data space is the selected space and player_token is either an X or O depending if 
	##the player or the computer made the move
	def update_board_data(self , space , player_token):
		self.board_data[int(space) - 1] = player_token
	
	def get_board_data(self):
		return self.board_data
	def get_board_moves_left(self):
		moves_left = []
		for items in self.board_data:
			if items != 'X' or items != 'O':
				moves_left.append(items)
		return moves_left
	def check_for_ties(self):
		##a tie occurs if no moves are left and we have no winner
		return len(self.get_board_moves_left())
		
	##check all paths to see if the game has a winner
	def check_for_winner(self):
	
		##loop through the dictionary
		for key, value in self.board_winning_paths.iteritems():
			##player_token_count keeps track of how many player tokens we have in a row
			player_token_count = 0
			##cpu_token_count keeps track of how many computer tokens we have in a row
			cpu_token_count = 0
			##nested loop for the board rows that result in a win
			for board_positions in value:
				
				if (self.board_data[board_positions] == "X"):
					player_token_count += 1
				elif (self.board_data[board_positions] == "O"):
					cpu_token_count += 1
			if(player_token_count == 3):
				return "player wins"
			elif(cpu_token_count == 3):
				return "computer wins"
		##if no winner return false after we check every possible way to win
		return False
		
	##Check and see if someone can win, the X or O given as the second parameter determines who we are looking for
	##if so return the index that would win the game so we know where to place our O
	def is_game_winnable(self, token):
	##This starts off a lot like checking for winners, but the logic is a little different
		##loop through the dictionary of winnable paths
		for key, value in self.board_winning_paths.iteritems():
			##Keeping track of the empty spaces on a winning row
			##when the inner loop finishes if the length of this array is 1 we have a winnable spot
			##if both loops finish with no winnable spot we return false
			winnable_space = []
			##taken_spaces keeps track of what is taken, if 2 of these are taken we could have a win
			taken_spaces = []
			##nested loop for the board rows that result in a win
			for board_positions in value:
				if (self.board_data[board_positions] == token):
					taken_spaces.append(board_positions)
				elif (self.board_data[board_positions] != "X" or self.board_data[board_positions] != "O"):
					winnable_space.append(board_positions)
			if len(winnable_space) == 1 and len(taken_spaces) == 2:
				print winnable_space
				return winnable_space[0]
		return False
	def get_open_corners(self):
		open_corners = []
		for corner in self.corners:
			if corner != "X" or corner != "O":
				open_corners.append(corner)
		return open_corners
	##helper method checks opposite corners to see if we moved their already, if so we want to make that move so there is a
	##bigger chance at winning
	##def check_opposite_corners(self, corner):
	##	if corner == 0
	##		##look at opposite corners
	##		if self.board_data[2] == "3" or self.board_data[6] == "7" or 
	
	##returns available the best corner to move to
	def get_corner_move(self):
		##first lets check and see what corners are open
		open_corners = self.get_open_corners()
		open_corners_size = len(open_corners)
		print open_corners_size
		##if its empty return false
		if open_corners_size == 0:
			return false
		elif open_corners_size == 1:
			##return the number since that is the only open corner
			return open_corner[0]
		else:
			##randomly chose what corner we want
			return random.choice(open_corners)
			
		