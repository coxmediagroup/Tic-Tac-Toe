# tic tac toe game where AI never loses
# Ravi Basawa as part of Cox Communications Radio test assignment
# assumption: AI takes first move
# algorithm: a comprehensive state transition design deemed 
#            practical because the above assumption and the
#            characteristic board symmetry reduces the size
#            of the table to manageable and intellible level
# initial stage - naive tic tac toe
# next stage - intelligent ai with rules to win and block and be naive as last resort
# tested - ran 10000 moves within minute (54s), no errors or ai losses
# 100 moves in 0.6 seconds so approx 6ms per op includes reads
import sys
import os 
import time 
import random
import re
from datetime import datetime



board=""
boardreset="0123A5678"
validhumaninput=["0","1","2","3","4","5","6","7","8","9"]

reset="GAME RESET AND RESTARTED, A IS AI WHILE H IS HUMAN, A HAS GONE FIRST ALREADY"
invalid="INPUT NEEDS TO BE IN RANGE 1..8 TO MARK BOARD OR 9 TO RESET BOARD, BOARD UNCHANGED"
occupied="SQUARE ALREADY FILLED, NO ENTRY MADE, BOARD UNCHANGED"
entered="HUMAN 'H' ENTERED SUCCESFULLY INTO SQUARE "
win="AI WINS GAME, RESET WITH 9 TO PLAY AGAIN"
draw="AI DRAWS GAME, RESET WITH 9 TO PLAY AGAIN"
loss="AI LOSES GAME, SHOULD NEVER HAPPEN, RESET WITH 9 TO PLAY AGAIN"
block="AI MADE BLOCKING MOVE"
naive="AI MADE NAIVE MOVE"

def tictactoeboard(humaninput):

   # create board if absent
   if not os.path.exists('board'):
      boardfile = open('board', 'w')
      boardfile.write(boardreset)
      boardfile.close()

   board = open('board').read()

   # invalid
   if humaninput not in validhumaninput:
      print invalid
      print board[0:3] + "\n" + board[3:6] + "\n" + board[6:9]
      return
   # reset
   elif humaninput == '9':
      board = boardreset
      boardfile = open('board', 'w')
      boardfile.write(boardreset)
      boardfile.close()
      print reset
      print board[0:3] + "\n" + board[3:6] + "\n" + board[6:9]
      return
   # occupied
   elif board[int(humaninput)] != humaninput:
   	  print occupied
   	  print board[0:3] + "\n" + board[3:6] + "\n" + board[6:9]
   	  return
   else:
      # entered
      board = board.replace(humaninput, 'H')
      boardfile = open('board', 'w')
      boardfile.write(board)
      boardfile.close()
      print entered + humaninput
      print board[0:3] + "\n" + board[3:6] + "\n" + board[6:9]

   # check if human won (should not occur, middle square is always ai A
   if ((re.search(r"HHH......",board)) or 
      (re.search(r"..H..H..H",board)) or 
      (re.search(r"......HHH",board)) or
      (re.search(r"H..H..H..",board))):
      boardfile = open('board', 'w')
      boardfile.write(board)
      boardfile.close()
      print loss
      print board[0:3] + "\n" + board[3:6] + "\n" + board[6:9]
      boardfile = open('board', 'w')
      boardfile.write(boardreset)
      boardfile.close()
      board = open('board').read()
      print reset
      print board[0:3] + "\n" + board[3:6] + "\n" + board[6:9]
      return

   # check if board is full for draw
   full=True
   for b in board:
      if b not in ['A','H']:
         full=False
   if full == True:
   	  boardfile = open('board', 'w')
   	  boardfile.write(board)
   	  boardfile.close()
   	  print draw
   	  print board[0:3] + "\n" + board[3:6] + "\n" + board[6:9]
   	  boardfile = open('board', 'w')
   	  boardfile.write(boardreset)
   	  boardfile.close()
   	  board = open('board').read()
   	  print reset
   	  print board[0:3] + "\n" + board[3:6] + "\n" + board[6:9]
   	  return
   
   # ai win
   aiwon = False
   if board[0] == 'A' and board[1] == 'A' and board[2] == '2':
   		board = board.replace('2', 'A')
   		aiwon = True
   elif board[0] == 'A' and board[2] == 'A' and board[1] == '1':
   		board = board.replace('1', 'A')
   		aiwon = True
   elif board[1] == 'A' and board[2] == 'A' and board[0] == '0':
   		board = board.replace('0', 'A')
   		aiwon = True
   elif board[3] == 'A' and board[4] == 'A' and board[5] == '5':
   		board = board.replace('5', 'A')
   		aiwon = True
   elif board[3] == 'A' and board[5] == 'A' and board[4] == '4':
   		board = board.replace('4', 'A')
   		aiwon = True
   elif board[4] == 'A' and board[5] == 'A' and board[3] == '3':
   		board = board.replace('3', 'A')
   		aiwon = True
   elif board[6] == 'A' and board[7] == 'A' and board[8] == '8':
   		board = board.replace('8', 'A')
   		aiwon = True
   elif board[6] == 'A' and board[8] == 'A' and board[7] == '7':
   		board = board.replace('7', 'A')
   		aiwon = True
   elif board[7] == 'A' and board[8] == 'A' and board[6] == '6':
   		board = board.replace('6', 'A')
   		aiwon = True
   elif board[0] == 'A' and board[3] == 'A' and board[6] == '6':
   		board = board.replace('6', 'A')
   		aiwon = True
   elif board[0] == 'A' and board[6] == 'A' and board[3] == '3':
   		board = board.replace('3', 'A')
   		aiwon = True
   elif board[3] == 'A' and board[6] == 'A' and board[0] == '0':
   		board = board.replace('0', 'A')
   		aiwon = True
   elif board[1] == 'A' and board[4] == 'A' and board[7] == '7':
   		board = board.replace('7', 'A')
   		aiwon = True
   elif board[1] == 'A' and board[7] == 'A' and board[4] == '4':
   		board = board.replace('4', 'A')
   		aiwon = True
   elif board[4] == 'A' and board[7] == 'A' and board[1] == '1':
   		board = board.replace('1', 'A')
   		aiwon = True
   elif board[2] == 'A' and board[5] == 'A' and board[8] == '8':
   		board = board.replace('8', 'A')
   		aiwon = True
   elif board[2] == 'A' and board[8] == 'A' and board[5] == '5':
   		board = board.replace('5', 'A')
   		aiwon = True
   elif board[5] == 'A' and board[8] == 'A' and board[2] == '2':
   		board = board.replace('2', 'A')
   		aiwon = True
   elif board[0] == 'A' and board[4] == 'A' and board[8] == '8':
   		board = board.replace('8', 'A')
   		aiwon = True
   elif board[0] == 'A' and board[8] == 'A' and board[4] == '4':
   		board = board.replace('4', 'A')
   		aiwon = True
   elif board[4] == 'A' and board[8] == 'A' and board[0] == '0':
   		board = board.replace('0', 'A')
   		aiwon = True
   elif board[2] == 'A' and board[4] == 'A' and board[6] == '6':
   		board = board.replace('6', 'A')
   		aiwon = True
   elif board[2] == 'A' and board[6] == 'A' and board[4] == '4':
   		board = board.replace('4', 'A')
   		aiwon = True
   elif board[4] == 'A' and board[6] == 'A' and board[2] == '2':
   		board = board.replace('2', 'A')
   		aiwon = True
   if aiwon == True:
    	boardfile = open('board', 'w')
    	boardfile.write(board)
    	boardfile.close()
    	print win
    	print board[0:3] + "\n" + board[3:6] + "\n" + board[6:9]
    	boardfile = open('board', 'w')
    	boardfile.write(boardreset)
    	boardfile.close()
    	board = open('board').read()
    	print reset
    	print board[0:3] + "\n" + board[3:6] + "\n" + board[6:9]
    	return 
   		
   # human block 
   humanblock = False
   if board[0] == 'H' and board[1] == 'H' and board[2] == '2':
   		board = board.replace('2', 'A')
   		humanblock = True
   elif board[0] == 'H' and board[2] == 'H' and board[1] == '1':
   		board = board.replace('1', 'A')
   		humanblock = True
   elif board[1] == 'H' and board[2] == 'H' and board[0] == '0':
   		board = board.replace('0', 'A')
   		humanblock = True
   elif board[2] == 'H' and board[5] == 'H' and board[8] == '8':
   		board = board.replace('8', 'A')
   		humanblock = True
   elif board[2] == 'H' and board[8] == 'H' and board[5] == '5':
   		board = board.replace('5', 'A')
   		humanblock = True
   elif board[5] == 'H' and board[8] == 'H' and board[2] == '2':
   		board = board.replace('2', 'A')
   		humanblock = True
   elif board[6] == 'H' and board[7] == 'H' and board[8] == '8':
   		board = board.replace('8', 'A')
   		humanblock = True
   elif board[6] == 'H' and board[8] == 'H' and board[7] == '7':
   		board = board.replace('7', 'A')
   		humanblock = True
   elif board[7] == 'H' and board[8] == 'H' and board[6] == '6':
   		board = board.replace('6', 'A')
   		humanblock = True
   if humanblock == True:
    	boardfile = open('board', 'w')
    	boardfile.write(board)
    	boardfile.close()
    	print block
    	print board[0:3] + "\n" + board[3:6] + "\n" + board[6:9]
    	# check whether board full
        full=True
        for b in board:
        	if b not in ['A','H']:
        		full=False
        if full == True:
            print draw
            print board[0:3] + "\n" + board[3:6] + "\n" + board[6:9]
            boardfile = open('board', 'w')
            boardfile.write(boardreset)
            boardfile.close()
            board = open('board').read()
            print reset
            print board[0:3] + "\n" + board[3:6] + "\n" + board[6:9]
        return 

   # ai naive move
   ainaivemove = False
   for bi in range(len(board)):
	    if board[bi] not in ['A','H']:
	       board = board.replace(str(bi), 'A')
	       ainaivemove = True
	       break
   if ainaivemove == True:
    	boardfile = open('board', 'w')
    	boardfile.write(board)
    	boardfile.close()
    	print naive
    	print board[0:3] + "\n" + board[3:6] + "\n" + board[6:9]
    	# check whether board full
        full=True
        for b in board:
        	if b not in ['A','H']:
        		full=False
        if full == True:
            print draw
            print board[0:3] + "\n" + board[3:6] + "\n" + board[6:9]
            boardfile = open('board', 'w')
            boardfile.write(boardreset)
            boardfile.close()
            board = open('board').read()
            print reset
            print board[0:3] + "\n" + board[3:6] + "\n" + board[6:9]
    	return 

   
  

# 1..8 : Mark Board ('H')
# 9    : Reset Board
myhumaninput = '9'
print tictactoeboard(myhumaninput)
a = datetime.now()
print a
i=0
while i < 100:
	myhumaninput=str(random.randint(0,9))
	print myhumaninput
	print tictactoeboard(myhumaninput)
	print "\n"
	i = i + 1
b = datetime.now()
print b
print (b-a).seconds
