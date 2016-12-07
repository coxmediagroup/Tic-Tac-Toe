"""
.. module:: ticTacToe
	:plataform: Unix, Windows
	:synopsis: This module its the engine of the Tic Tac Toe Board and the engine of the CPU Player for Tic Tac Toe
	
.. moduleauthor:: Ricardo Tercero Solis <tercero3@hotmail.com>
"""

class TicTacToeCPU:
    """This Class is the engine for CPU Player.

    You need to call first the TicTacToeEngine class to get board info for the CPU Player

    """

	current = [
		[None , None , None ,] ,
		[None , None , None ,] ,
		[None , None , None ,] ,
	]
	opponent = []
	cpu = []
	blank = []
	moves = 9
	cpu_peace = None
	opp_peace = None
	
	WINS = [
		['00' , '01' , '02' ,] ,
		['10' , '11' , '12' ,] ,
		['20' , '21' , '22' ,] ,
		['00' , '11' , '22' ,] ,
		['20' , '11' , '02' ,] ,
		['00' , '10' , '20' ,] ,
		['01' , '11' , '21' ,] ,
		['02' , '12' , '22' ,] ,
	]
	
	CORNERS = [
		{ 'x' : 0 , 'y' : 0 } ,
		{ 'x' : 0 , 'y' : 2 } ,
		{ 'x' : 2 , 'y' : 2 } ,
		{ 'x' : 2 , 'y' : 0 } ,
	]
	
	SIDES = [
		{ 'x' : 0 , 'y' : 1 } ,
		{ 'x' : 1 , 'y' : 0 } ,
		{ 'x' : 2 , 'y' : 1 } ,
		{ 'x' : 1 , 'y' : 2 } ,
	]
	
	def __init__(self , current = None , moves = None , cpu_peace = None , opp_peace = None):
	    """Initialize the class.

	    :param current: The Current state of the game board.
	    :type current: Array.
	    :param moves: The number of remain moves in the game.
	    :type moves: int.

	    """
		if current:
			self.current = current
			print "current %s" % self.current
		else:
			raise Exception("PARAMETERS")
		if moves:
			self.moves = moves
		else:
			raise Exception("PARAMETERS")
		if cpu_peace:
			self.cpu_peace = cpu_peace
		else:
			raise Exception("PARAMETERS")
		if opp_peace:
			self.opp_peace = opp_peace
		else:
			raise Exception("PARAMETERS")
		self.opponent = self.getState(self.opp_peace)
		self.cpu = self.getState(self.cpu_peace)
		self.blank = self.getState(None)
		
	def getMove(self):
	    """This function figure the next move for CPU Player.

	    :returns:  int, int -- Return the X and Y position in the board of the next move.

	    """
		if self.isFirstMove():
			#Is the first move
			import random
			if random.randrange(0,2) == 0:
				#if 0 the first move is hitting center
				return self.getCenter()
			else:
				#if 0 the first move is hitting corner
				return self.getFreeCorner()
		else:
			#Is not the first move
			print "%s is 3rd : %s" % (self.moves , self.isThirdMove())
			if self.isThirdMove():
				if self.hasCenter(self.cpu):
					if self.hasCorner(self.opponent):
						x = self.opponent[0][0]
						y = self.opponent[0][1]
						return self.getOppositeCorner(x , y)
					else:
						x = self.opponent[0][0]
						y = self.opponent[0][1]
						return self.getAnyFurthestCorner(x , y)
				if self.hasCorner(self.cpu):
					if self.hasCenter(self.opponent):
						x = self.cpu[0][0]
						y = self.cpu[0][1]
						print "outer %s %s" %self.getOppositeCorner(x , y)					
						return self.getOppositeCorner(x , y)
					else:
						x = self.cpu[0][0]
						y = self.cpu[0][1]
						return self.getAsideCorner(x , y)
			elif self.couldOppenetWin():
				return self.blockOponnet()
			else:
				paths = self.getWiningPaths(player = self.cpu , opponent = self.opponent , moves = 1)
				print "winning pats %s" %paths
				for path in paths:
					for possible in path['possible_moves']:
						x = possible[0]
						y = possible[1]
						return x , y
				paths = self.getWiningPaths(player = self.cpu , opponent = self.opponent , moves = 2)
				for path in paths:
					for possible in path['possible_moves']:
						x = possible[0]
						y = possible[1]
						if self.isSide(x = x , y = y):
							return x , y
					for possible in path['possible_moves']:
						x = possible[0]
						y = possible[1]
						if self.isCenter(x = x , y = y):
							return x , y
					for possible in path['possible_moves']:
						x = possible[0]
						y = possible[1]
						if self.isCorner(x = x , y = y):
							return x , y
				x , y = self.getCenter()
				if x and y:
					return x , y
				x , y = self.getFreeCorner()
				if x and y:
					return x , y
				return self.getAnyFreePosition()
			return None , None
			

	def couldOppenetWin(self):
	    """Figure if the opponent has a winning move in their next ove.

	    :returns:  bool -- True if Yes and False if No.

	    """
		if len(self.opponent) > 1:
			paths = self.getWiningPaths(player = self.opponent , opponent = self.cpu , moves = 1)
			if len(paths) > 0:
				return True
		return False
		
	def blockOponnet(self):
	    """Figure the position to block the winning move of the opponent.

	    :returns:  int, int -- Return the X and Y position in the board of the next move.

	    """
		paths = self.getWiningPaths(player = self.opponent , opponent = self.cpu , moves = 1)
		print paths
		for path in paths:
			for possible in path['possible_moves']:
				x = possible[0]
				y = possible[1]
				if self.isCenter(x = x , y = y):
					return x , y
		for path in paths:
			for possible in path['possible_moves']:
				x = possible[0]
				y = possible[1]
				if self.isSide(x = x , y = y):
					return x , y
		for path in paths:
			for possible in path['possible_moves']:
				x = possible[0]
				y = possible[1]
				if self.isCorner(x = x , y = y):
					return x , y
		return None , None
			
	def getWiningPaths(self , player , opponent , moves = None):
	    """Return the Coordinate of the Opposite Corner.
	
	    :param player: The choice positions of the player
	    :type player: Array.
	    :param opponent: The choice positions of the player's opponent.
	    :type opponent: Array.
	    :param moves: Number of moves in the path needed to win.
	    :type moves: int.
	    :returns:  Array -- Returns the possible winning paths.

	    """
		paths = []
		for path in self.WINS:
			moves_to_win = 3
			valid = True
			possible_moves = []
			for position in path:
				if position in player:
					moves_to_win = moves_to_win - 1
				elif position in opponent:
					valid = False
					break
				else:
					possible_moves.append(position)
			paths.append({ 'path' : path , 'moves_to_win' : moves_to_win , 'valid' : valid , 'possible_moves' : possible_moves })
		aux = []
		for path in paths:
			if path['valid'] and path['moves_to_win'] < 3:
				if moves:
					if path['moves_to_win'] <= moves:
						aux.append(path)
				else:
					aux.append(path)
		return aux

	def getState(self , value):
	    """Return choice positions.
	
	    :param value: The figure to look in the board (X or O)
	    :type value: str.
	    :returns:  Array -- Returns the possible winning paths.

	    """
		state = []
		for x , line in enumerate(self.current):
			for y , pos in enumerate(line):
				if pos == value:
					p = "%s%s" %(x,y)
					state.append(p)
		return state

	def isCorner(self , x , y):
	    """Return if the coordinate is corner.
	
	    :param x: The X coordinate
	    :type x: int.
	    :param y: The Y coordinate
	    :type y: int.
	    :returns:  boo -- Returns True if Yes or False if not.

	    """
		for corner in self.CORNERS:
			if str(corner['x']) == str(x) and str(corner['y']) == str(y):
				return True
		return False
		
	def isSide(self , x , y):
	    """Return if the coordinate is side.
	
	    :param x: The X coordinate
	    :type x: int.
	    :param y: The Y coordinate
	    :type y: int.
	    :returns:  boo -- Returns True if Yes or False if not.

	    """
		for side in self.SIDES:
			if str(side['x']) == str(x) and str(side['y']) == str(y):
				return True
		return False
		
	def isCenter(self , x , y):
	    """Return if the coordinate is center.
	
	    :param x: The X coordinate
	    :type x: int.
	    :param y: The Y coordinate
	    :type y: int.
	    :returns:  boo -- Returns True if Yes or False if not.

	    """
		if '1' == str(x) and '1' == str(y):
			return True
		return False
	
	def isFirstMove(self):
	    """Figures if the CPU Player has the First Move of the game.

	    :returns:  bool -- True if Yes and False if No.

	    """
		if self.moves == 9:
			return True
		return False
		
	def isThirdMove(self):
	    """Figures if the CPU Player has the Third Move of the game.

	    :returns:  bool -- True if Yes and False if No.

	    """
		if self.moves == 7:
			return True
		return False
		
	def getCenter(self):
	    """Returns the X and Y of the Center of the Board.

	    :returns:  int, int -- Return the X and Y Center of the Board.

	    """
		return self.getPosition(1 , 1)
		
	def getAnyFreePosition(self):
	    """Returns the X and Y of any Random Free Position.

	    :returns:  int, int -- Return the X and Y Center of the Board.

	    """
		if len(self.blank) > 0:
			import random
			index = random.randrange(0,len(self.blank))
			x , y = self.getPosition(int(self.blank[index][0]) , int(self.blank[index][1]))
			return int(x) , int(y)
		return None , None
		
	def getFreeCorner(self):
	    """Returns the X and Y of a Free Corner.

	    :returns:  int, int -- Returns the X and Y of a Free Corner.

	    """
		for position in self.CORNERS:
			x , y = self.getPosition(position['x'] , position['y'])
			if x and y:
				return x , y
		return None , None
		
	def getOppositeCorner(self , x , y):
	    """Return the Coordinate of the Opposite Corner.
	
	    :param x: The X coordinate
	    :type x: int.
	    :param y: The Y coordinate.
	    :type y: int.
	    :returns:  int, int -- Returns the X and Y of the Coordinate of the Opposite Corner.

	    """
		if x and y:
			if int(x) == 0 and int(y) == 0:
				return self.getPosition(2 , 2)
			elif int(x) == 2 and int(y) == 2:
				return self.getPosition(0 , 0)
			elif int(x) == 0 and int(y) == 2:
				return self.getPosition(2 , 0)
			elif int(x) == 2 and int(y) == 0:
				return self.getPosition(0 , 2)
		return None , None
		
	def getAsideCorner(self , x , y):
	    """Return the Coordinate of the available Corner Horizontal or Vertical.
	
	    :param x: The X coordinate
	    :type x: int.
	    :param y: The Y coordinate.
	    :type y: int.
	    :returns:  int, int -- Returns the X and Y of the available Corner Horizontal or Vertical.

	    """
		if x and y:
			if int(x) == 0 and int(y) == 0:
				x, y = self.getPosition(0 , 2)
				if x and y:
					return x , y
				return self.getPosition(2 , 0)
			elif int(x) == 2 and int(y) == 2:
				x, y = self.getPosition(0 , 2)
				if x and y:
					return x , y
				return self.getPosition(2 , 0)
			elif int(x) == 0 and int(y) == 2:
				x, y = self.getPosition(0 , 0)
				if x and y:
					return x , y
				return self.getPosition(2 , 0)
			elif int(x) == 2 and int(y) == 0:
				x, y = self.getPosition(0 , 0)
				if x and y:
					return x , y
				return self.getPosition(2 , 2)
		return None , None
		
	def getOppositeSide(self , x , y):
	    """Return the Coordinate of the opposite position.
	
	    :param x: The X coordinate
	    :type x: int.
	    :param y: The Y coordinate.
	    :type y: int.
	    :returns:  int, int -- Returns the X and Y of the opposite Side.

	    """
		if x and y:
			if int(x) == 0 and int(y) == 1:
				return self.getPosition(2 , 1)
			elif int(x) == 1 and int(y) == 0:
				return self.getPosition(1 , 2)
			elif int(x) == 2 and int(y) == 1:
				return self.getPosition(0 , 1)
			elif int(x) == 1 and int(y) == 2:
				return self.getPosition(1 , 0)
		return None , None
		
	def getPosition(self , x , y):
	    """Check if the coordinate is available.
	
	    :param x: The X coordinate
	    :type x: int.
	    :param y: The Y coordinate
	    :type y: int.
	    :returns:  int , int -- Returns X , Y coordinates if are available or None , None if not.

	    """	
		if self.current[x][y]:
			return None , None
		return x , y
		
	def hasCorner(self , player):
	    """Figure if the Player has a Corner Position.
	
	    :param player: The choice positions of the player
	    :type player: Array.
	    :returns:  boo -- Return True if Yes, False if not.

	    """
		for position in player:
			for corner in self.CORNERS:
				if position[0] == str(corner['x']) and position[1] == str(corner['y']):
					return True
		return False
	
	def hasCenter(self , player):
	    """Figure if the Player has the Center of the Board.
	
	    :param player: The choice positions of the player
	    :type player: Array.
	    :returns:  boo -- Return True if Yes, False if not.

	    """
		for position in player:
			if position[0] == '1' and position[1] == '1':
				return True
		return False
	
	def getAnyFurthestCorner(self , x , y):
	    """Returns the Furthest Corners based on the Parameters.
	
	    :param x: The X coordinate
	    :type x: int.
	    :param y: The Y coordinate.
	    :type y: int.
	    :returns:  Array -- Returns an Array with free Furthest Corner.

	    """
		pos = self.getFurthestCorners(x , y)
		if len(pos) > 0:
			import random
			index = random.randrange(0,len(pos))
			x , y = self.getPosition(int(pos[index][0]) , int(pos[index][1]))
			return int(x) , int(y)
		return None , None
	
	def getFurthestCorners(self , x , y):
	    """Returns the X and Y of the Furthest Corner based on the Parameters.
	
	    :param x: The X coordinate
	    :type x: int.
	    :param y: The Y coordinate.
	    :type y: int.
	    :returns:  int, int -- Returns the X and Y of a Free Corner.

	    """
		if int(x) == 0 and int(y) == 1:
			return [ '20' , '22' ]
		if int(x) == 1 and int(y) == 2:
			return [ '02' , '22' ]
		if int(x) == 1 and int(y) == 0:
			return [ '00' , '20' ]
		if int(x) == 2 and int(y) == 1:
			return [ '00' , '02' ]
		return []

class TicTacToeEngine:
    """This Class is the engine for the board.

    """

	_CROSS = 'X'
	_NOUGHT = 'O'
	current = [
		[None , None , None ,] ,
		[None , None , None ,] ,
		[None , None , None ,] ,
	]
	wins = [
		['00' , '01' , '02' ,] ,
		['10' , '11' , '12' ,] ,
		['20' , '21' , '22' ,] ,
		['00' , '11' , '22' ,] ,
		['20' , '11' , '02' ,] ,
		['00' , '10' , '20' ,] ,
		['01' , '11' , '21' ,] ,
		['02' , '12' , '22' ,] ,
	]
	cross = []
	nought = []
	blank = []
	moves = 9
	last = {
		'value'	:	None ,
		'x'		: 	None ,
		'y'		:	None ,
	}
	
	def setLast(self , last):
	    """Set the Last Move in the Game.

	    """
		if last:
			self.last = last
	
	def setBoard(self , state):
	    """Translate a string representing the state of the board.

	    """
		x = 0
		y = 0
		for s in state:
			if s == "N":
				self.current[x][y] = None
			elif s == self._CROSS or s == self._NOUGHT:
				self.current[x][y] = s
				self.moves = self.moves - 1
			y = y + 1
			if y == 3:
				y = 0
				x = x + 1
			if x == 3:
				break

	def getBoard(self):
	    """Get the String representing the board.

		:returns: str - Get the String representing the board

	    """
		state = ""
		for x , line in enumerate(self.current):
			for y , pos in enumerate(line):
				if pos is None:
					pos = "N"
				state = "%s%s" %(state , pos)
		return state

	def getLog(self):
	    """Get the String of the move of the player.

		:returns: str - Get the String of the move of the player

	    """
		msg = "Puts %s in the" % self.last['value']
		if self.last['y'] == 0 and self.last['x'] == 0:
			msg  = "%s %s" % (msg , "Top Left Corner")
		elif self.last['y'] == 0 and self.last['x'] == 1:
			msg  = "%s %s" % (msg , "Middle Left Position")
		elif self.last['y'] == 0 and self.last['x'] == 2:
			msg  = "%s %s" % (msg , "Bottom Right Corner")
		elif self.last['y'] == 1 and self.last['x'] == 0:
			msg  = "%s %s" % (msg , "Top Middle Position")
		elif self.last['y'] == 1 and self.last['x'] == 1:
			msg  = "%s %s" % (msg , "Center Position")
		elif self.last['y'] == 1 and self.last['x'] == 2:
			msg  = "%s %s" % (msg , "Bottom Middle Position")
		elif self.last['y'] == 2 and self.last['x'] == 0:
			msg  = "%s %s" % (msg , "Top Right Corner")
		elif self.last['y'] == 2 and self.last['x'] == 1:
			msg  = "%s %s" % (msg , "Middle Right Position")
		elif self.last['y'] == 2 and self.last['x'] == 2:
			msg  = "%s %s" % (msg , "Bottom Right Corner")
		return msg
	
	def initializeGame(self):
	    """Set the values of the board ready to start the game.

	    """
		self.cross = []
		self.nought = []
		self.blank = []
		self.moves = 9
		self.current = [
			[None , None , None ,] ,
			[None , None , None ,] ,
			[None , None , None ,] ,
		]
	
	def isDraw(self):
	    """Check if the game is Draw.
	
		:returns: boo - True if yes or False if not

	    """
		if len(self.blank) == 9 or self.moves == 0:
			return True
		return False
	
	def hasWon(self , state):
	    """Check if the state has any winning path full.
	
	    :param state: The coordinates of the positions that has a value (X or Y)
	    :type state: Array.
		:returns: boo - True if yes or False if not

	    """
		if self.moves == 9:
			return False
		for win in self.wins:
			hits = 0
			for p in win:
				if p in state:
					hits = hits + 1
				else:
					break
			if hits == 3:
				return True
		return False
		
	def getState(self , value):
	    """Get the positions that has the value.
	
	    :param value: Either X or O
	    :type value: str.
		:returns: Array - The coordinates of the positions that has the value

	    """
		state = []
		for x , line in enumerate(self.current):
			for y , pos in enumerate(line):
				if pos == value:
					p = "%s%s" %(x,y)
					state.append(p)
		return state
		
	def setMovement(self, value , x , y):
	    """Set the Choice if the position if available.
	
	    :param value: Either X or O
	    :type value: str.
	    :param x: The X Coordinate
	    :type x: int.
	    :param y: The X Coordinate
	    :type y: int.
		:raises: Exception

	    """
		x = int(x)
		y = int(y)
		if x > 2:
			raise Exception("The Value of X should be 0 , 1 or 3")
		if y > 2:
			raise Exception("The Value of Y should be 0 , 1 or 3")
		if self.current[x][y]:
			raise Exception("This Position is Already Taken")
		self.current[x][y] = value
		self.moves = self.moves - 1
		self.last = {
			'value'	:	value ,
			'x'		: 	x ,
			'y'		:	y ,
		}
		
	def move(self , value , x , y):
	    """Try to take the position in the Coordinate X and Y, verify if the Player Won or if the game has Draw.
	
	    :param value: Either X or O
	    :type value: str.
	    :param x: The X Coordinate
	    :type x: int.
	    :param y: The X Coordinate
	    :type y: int.
		:raises: Exception

	    """
		if value == self.last['value']:
			raise Exception("You can not Move Because is not Your Turn")
		self.setMovement(value , x , y)
		state = self.getState(value)
		self.blank = self.getState(None)
		if self.hasWon(state):
			msg = "%s has won" % value
			msg = "WON"
			raise Exception(msg)
		elif self.isDraw():
			msg = "Game is Draw"
			msg = "DRAW"
			raise Exception(msg)

		