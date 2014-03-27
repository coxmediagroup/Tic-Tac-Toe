##Class file for the tic-tac-toe board
##Contains board state data and logic for winning/finding empty spots for the computer to use
import random

class GameBoard(object):
	
	def __init__(self):
		self.board_data = ["1" , "2" , "3" , "4" , "5" , "6" , "7" , "8" , "9"]
		
	##board_data contains all the data that goes into the gameboard, it will contain numbers for spaces player can move to,
	##or spaces that contain a move (X or O).
	board_data = []	
	
	##The following data is used to help the computer know whats open and make the right decision
	corners = [ 1 , 3 , 7 , 9 ]
	sides = [ 2 , 3 , 5 , 7 ]
	
	##This dictionary contains all 8 possible way to win the game
	##1 and 2 are the horizontal wins
	##3-6 are vertical wins
	##6-8 are horizontal wins
	board_winning_paths = {
		1:[ 1 , 5 , 9 ] , 2:[ 3 , 5 , 7 ] , 3:[ 1 , 4 , 7 ] , 4:[ 2 , 5 , 8 ] ,
		5:[ 3 , 6 , 9 ] , 6:[ 1 , 2 , 3 ] , 7:[ 4 , 5 , 6 ] , 8:[ 7 , 8 , 9 ]
	}
	
	##This dictionary contains opposite corners we need to choose from, if the user is first and selects a corner spot
	opposite_corner_choices = {
		1:[ 3 , 7 ] , 3:[ 1 , 9 ] , 
		7:[ 1 , 3] , 9:[ 3 , 7 ]
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
	def update_board_data( self , space , player_token ):
		self.board_data[int(space) - 1] = player_token
	
	def get_board_data( self ):
		return self.board_data
		
	def get_board_moves_left( self ):
		moves_left = []
		for items in self.board_data:
			if items != 'X' and items != 'O':
				moves_left.append(items)
		return moves_left
	##Checks and sees if a corner was taken as the first move
	##If we have 2 X's return false as its no longer the first turn
	def check_players_first_move( self ):
		for corner in self.corners:
			if self.board_data[ corner - 1 ] == "X":
				return True
		return False
	
	##check all paths to see if the game has a winner
	def check_for_winner( self ):
		##first lets make sure there isnt a tie
		if ( len( self.get_board_moves_left() ) == 0):
			return "tie"
			
		##loop through the dictionary
		for key, value in self.board_winning_paths.iteritems():
			##player_token_count keeps track of how many player tokens we have in a row
			player_token_count = 0
			##cpu_token_count keeps track of how many computer tokens we have in a row
			cpu_token_count = 0
			##nested loop for the board rows that result in a win
			for board_positions in value:

				if ( self.board_data[board_positions - 1] == "X" ):
					player_token_count += 1
				elif ( self.board_data[board_positions - 1] == "O" ):
					cpu_token_count += 1
					
			if(player_token_count == 3):
				return "player wins"
			elif(cpu_token_count == 3):
				return "computer wins"
				
		##if no winner return false after we check every possible way to win
		return False
		
	##Check and see if someone can win, the X or O given as the second parameter determines who we are looking for
	##if so return the index that would win the game so we know where to place our O
	def is_game_winnable( self, token ):
	##This starts off a lot like checking for winners, but the logic is a little different
		##loop through the dictionary of winnable paths
		for key, value in self.board_winning_paths.iteritems():
			##nested loop for the board rows that result in a win
			##Keeping track of the empty spaces on a winning row
			##when this loop finishes if the length of this array is 1 we have a winnable spot
			##if both loops finish with no winnable spot we return false
			winnable_space = "-1"
			##taken_spaces keeps track of what is taken, if 2 of these are taken we could have a win
			taken_spaces = []
			for board_positions in value:
				if (self.board_data[board_positions - 1] == token):
					taken_spaces.append(board_positions)
				elif (self.board_data[board_positions - 1] != "X" and self.board_data[board_positions - 1] != "O"):
					winnable_space = board_positions
			if winnable_space != "-1" and len(taken_spaces) == 2:
				return winnable_space
		return False
	def get_open_corners( self ):
		open_corners = []
		for corner in self.corners:
			if self.board_data[corner - 1] != "X" and self.board_data[corner - 1] != "O":
				open_corners.append(corner)
		return open_corners
		
	def get_open_sides( self ):
		open_sides = []
		for side in self.sides:
			if self.board_data[side - 1] != "X" and self.board_data[side - 1] != "O":
				open_sides.append(side)
		return open_sides
	
	##returns available the best place to move to
	## spaceToCheck is either corner or side, which tells us how to proceed
	def get_move( self , space_to_check ):
		open_spaces = []
		open_spaces_size = []
		
		if(space_to_check == "corner"):
			##first lets check and see what corners are open
			open_spaces = self.get_open_corners()
			open_spaces_size = len(open_spaces)
		else:
			##Check and see what sides are open
			open_spaces = self.get_open_sides()
			open_spaces_size = len(open_spaces)
		
		##if its empty return false
		if open_spaces_size == 0:
			return false
		elif open_spaces_size == 1:
			##return the number since that is the only open corner
			return open_spaces[0]
		else:
			##randomly chose what space we want
			return random.choice(open_spaces)
			
		