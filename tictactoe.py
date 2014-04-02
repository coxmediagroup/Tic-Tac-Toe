#!/usr/bin python
#	Tic Tac Toe
#	Danny Burrows
#
#	Implement a version of tic-tac-toe where a player plays against an AI bot where the AI never loses.

from Tkinter import Tk, Frame, Button
from ttk import Style, Label, Entry

# game class
# need the following
# -actual board array
# -list of open moves
# -is game over
# -who's turn
# -winner
# -mark a board slot
# -remove a mark
class gameState:
	def __init__(self):
		self.board = [0 for x in range(9)]
		self.winner = None

	def printBoard(self):
		print "%s | %s | %s" % (self.board[0], self.board[1], self.board[2])
		print "--+---+--"
		print "%s | %s | %s" % (self.board[3], self.board[4], self.board[5])
		print "--+---+--"
		print "%s | %s | %s" % (self.board[6], self.board[7], self.board[8])
		#print self.board

	def availMoves(self):
		moves = []
		for i,x in enumerate(self.board):
			if x == 0:
				moves.append(i)
		return moves

	def gameOver(self):
		# 0 1 2
		# 3 4 5
		# 6 7 8
		wins = [ (0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6) ]
		for i,j,k in wins:
			if self.board[i] == self.board[j] == self.board[k] and self.board[i] != 0:
				self.winner = self.board[i]
				return True

		if 0 not in self.board:
			self.winner = 3
			return True

		return False

	def makeMove(self, move, player):
		if move < 0 or move > 8:
			return False
		if not self.board[move]:
			self.board[move] = player
			return True
		return False

	def clearMove(self, move):
		self.board[move] = 0

	def boardState(self):
		return self.board

	def setBoard(self, array):
		self.board = self.__boardArray(array)

	def __boardArray(self, input):
		return (map(int,input.split()))

# class container for human player
# needs:
# -marker
# -get the move as an input
# --test move
# 
class human:
	def __init__(self, marker = 1, opponent = 2):
		self.marker = marker
		self.opponent = opponent
	
	def getMove(self, gameInstance):
		while True:
			nextMove = raw_input("What move? ")
			if gameInstance.makeMove(int(nextMove), self.marker):
				break
			else:
				print "Invalid move, please try again"

# class for AI moves
# need:
# miniMax function
# -implement via game trees, attempt to maximize AI moves to win, minimize players to lose
# -max and min functions, that work recursively on the current ply
# -evaluation of currently tested ply
class botAI:
	def __init__(self, marker = 2, opponent = 1):
		self.marker = marker
		self.opponent = opponent

	def miniMax(self, gameInstance):
		move = self.maxMove(gameInstance)[1]
		gameInstance.makeMove(move, self.marker)

	# bestMove location and bestMove value
	# value will be used to determine if the move is a good one or not, from eval game
	def maxMove(self, ply):
		bestMove = None
		bestValue = None
		# foreach childnode, find min
		# track both the move and the value, will need on upwards travesal
		for move in ply.availMoves():
			# for each move, make the move and test the result
			# if the move is not the best move, based on evaluation of each ply, then undo move
			ply.makeMove(move, self.marker)
			# base case
			if ply.gameOver():
				value = self.evalGame(ply)
			# recusive case
			else:
				value,testMove = self.minMove(ply)
			
			ply.clearMove(move)

			if value > bestValue or bestValue == None:
				bestValue = value
				bestMove = move

		return bestValue, bestMove

	# from psuedo, essentially the same, but swaping the logic checks
	def minMove(self, ply):
		bestMove = None
		bestValue = None
		# foreach childnode, find min
		# track both the move and the value, will need on upwards travesal
		for move in ply.availMoves():
			# for each move, make the move and test the result
			# if the move is not the best move, based on evaluation of each ply, then undo move
			ply.makeMove(move, self.opponent)
			# base case
			if ply.gameOver():
				value = self.evalGame(ply)
			# recusive case
			else:
				value,testMove = self.maxMove(ply)
			
			ply.clearMove(move)

			if value < bestValue or bestValue == None:
				bestValue = value
				bestMove = move

		return bestValue, bestMove

	def evalGame(self, ply):
		# check this ply has reached conclusion
		if ply.gameOver():
			# ai has won
			if ply.winner == self.marker:
				return 10
			# player has won
			elif ply.winner == self.opponent:
				return -10
		return 0 # default case

class GUI(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent, background="white")
		self.parent = parent
		self.bot = botAI()
		self.player = human()
		self.game = gameState()
		self.buttons = []
		self.initUI()

	def initUI(self):
		self.parent.title("Buttons")
		buttons = []
		Style().configure("TButton", font="serif 128")

		self.columnconfigure(0, pad=3)
		self.columnconfigure(1, pad=3)
		self.columnconfigure(2, pad=3)

		self.rowconfigure(0, pad=3)
		self.rowconfigure(1, pad=3)
		self.rowconfigure(2, pad=3)

		for x in range(9):
			handler = lambda x=x:self.updateBoard()
			self.buttons.append(Button(self,command=handler,text='-',height=4,width=4))
			self.buttons[-1].grid(row=(x / 3), column=(x % 3))

		self.pack()
	
	def makeMove(self, input):
		self.buttons[input]['text']=input
	
	def updateBoard(self):
		for i,x in enumerate(self.game.boardState()):
			if x == 1:
				self.buttons[i]['text'] = "X"
			elif x == 2:
				self.buttons[i]['text'] = "O"

def main():
	root = Tk()
	root.geometry("250x250+300+300")
	app = GUI(root)
	root.mainloop()

if __name__ == '__main__':
	main()

def testCase(gameState, expectedMove):
	bot = botAI()
	nextMove = bot.miniMax(gameState)
	#print nextMove
	if nextMove == expectedMove:
		print 'PASSED'
	else:
		print 'FAILED Expected ' + str(expectedMove) + ' Calculated ' + str(nextMove)
	

def runTests():
	# 0 1 2
	# 3 4 5
	# 6 7 8
	game = gameState()
	game.setBoard("0 0 1 0 2 1 0 0 0")
	testCase(game, 8)
	game.setBoard("0 0 0 0 0 0 0 0 0")
	testCase(game, 5)
	game.setBoard("1 1 2 2 2 1 0 0 0")
	testCase(game, 6)
	game.setBoard("1 0 0 1 2 0 0 0 0")
	testCase(game, 6)
	game.setBoard("2 1 1 0 2 0 0 0 0")
	testCase(game, 8)

def play():
	game = gameState()
	player = human()
	bot = botAI()
	game.printBoard()
	while True:
		
		player.getMove(game)
		print "\n"
		game.printBoard()
		if game.gameOver():
			print game.winner
			exit()
		
		bot.miniMax(game)
		print "\n"
		game.printBoard()
		if game.gameOver():
			print game.winner
			exit()
