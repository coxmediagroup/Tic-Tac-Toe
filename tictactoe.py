#!/usr/bin python
#	Tic Tac Toe
#	Danny Burrows
#
#	Implement a version of tic-tac-toe where a player plays against an AI bot where the AI never loses.

from Tkinter import Tk, Frame, Button
from ttk import Style, Label, Entry
import tkMessageBox as box

# game class
class gameState:
	def __init__(self):
		self.board = [0 for x in range(9)]
		self.winner = None
		self.startPlayer = 1

	def availMoves(self):
		moves = []
		for i,x in enumerate(self.board):
			if x == 0:
				moves.append(i)
		return moves

	def gameOver(self):
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

	def newGame(self):
		self.setBoard("0 0 0 0 0 0 0 0 0")

# class container for human player
class human:
	def __init__(self, marker = 1, opponent = 2):
		self.marker = marker
		self.opponent = opponent
	
	def makeMove(self, move, gameInstance):
		if gameInstance.makeMove(move, self.marker):
			return True
"""
	def getMove(self, gameInstance):
		while True:
			nextMove = raw_input("What move? ")
			if gameInstance.makeMove(int(nextMove), self.marker):
				break
			else:
				print "Invalid move, please try again"
"""
# class for AI moves
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
		self.whoBegins()
		self.gameStart()

	def initUI(self):
		self.parent.title("TicTacToe")
		buttons = []
		Style().configure("TButton")

		# layout for buttons
		self.columnconfigure(0, pad=3)
		self.columnconfigure(1, pad=3)
		self.columnconfigure(2, pad=3)

		self.rowconfigure(0, pad=3)
		self.rowconfigure(1, pad=3)
		self.rowconfigure(2, pad=3)

		for x in range(9):
			handler = lambda x=x: self.mark(x)
			self.buttons.append(Button(self,command=handler,text='-',height=4,width=4))
			self.buttons[-1].grid(row=(x / 3), column=(x % 3))

		self.pack()

	def whoBegins(self):
		result = box.askquestion("Who starts?", "Would you like to begin?")
		if result == "yes":
			self.game.startPlayer = 1
		else:
			self.game.startPlayer = 2

	def mark(self, input):
		# onclick, verify the move is valid and update it with the players marker
		if self.player.makeMove(input, self.game):
			self.updateBoard()
			if self.game.gameOver():
				self.gameOver()
			else:
				self.bot.miniMax(self.game)
				self.updateBoard()
				if self.game.gameOver():
					self.gameOver()
	
	def updateBoard(self):
		# update the buttons and disable the buttons that have been selected
		for i,x in enumerate(self.game.boardState()):
			if x == 1:
				self.buttons[i]['text'] = "X"
				self.buttons[i]['state'] = 'disabled'
				self.buttons[i]['disabledforeground'] = 'black'
			elif x == 2:
				self.buttons[i]['text'] = "O"
				self.buttons[i]['state'] = 'disabled'
				self.buttons[i]['disabledforeground'] = 'black'

	def resetBoard(self):
		self.game.setBoard("0 0 0 0 0 0 0 0 0")
		for x in self.buttons:
			x['text'] = '-'
			x['state'] = 'active'
	
	def gameOver(self):
		if self.game.winner == 1:
			title = "You have won!"
		elif self.game.winner == 2:
			title = "The computer has bested you!"
		else:
			title = "The cat wins!"
		result = box.askquestion("Game Over", title + "\nWould you like to play again?")
		if result == "yes":
			self.resetBoard()
			self.whoBegins()
			self.gameStart()
		else:
			exit()
	
	def gameStart(self):
		if self.game.startPlayer == 2:
			self.bot.miniMax(self.game)
			self.updateBoard()

def main():
	root = Tk()
	root.geometry("250x250+300+300")
	app = GUI(root)
	root.mainloop()

if __name__ == '__main__':
	main()
