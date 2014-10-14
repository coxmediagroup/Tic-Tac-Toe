#!/usr/local/bin/python
# tic tac toe app  where AI never loses
# Ravi Basawa as part of Cox Communications Radio test assignment
# assumption: AI takes first move
# one stop, works

import cgi
import cgitb; cgitb.enable()  # for troubleshooting
import sys
import os 
import time 
import random
import re
from datetime import datetime


board=""
boardreset="0123A5678"
validhumaninput=["0","1","2","3","4","5","6","7","8","9"]

reset="<h3>GAME RESET AND RESTARTED, A IS AI, H IS HUMAN, A HAS GONE FIRST</h3>"
invalid="<h3>INPUT NEEDS TO BE IN RANGE 1..8 OR BE 9 TO RESET BOARD</h3>"
occupied="<h3>SQUARE ALREADY FILLED</h3>"
entered="<h3>HUMAN 'H' ENTERED SUCCESFULLY INTO SQUARE "
win="<h3>AI WINS GAME</h3>"
draw="<h3>AI DRAWS GAME</h3>"
loss="<h3>AI LOSES GAME, SHOULD NEVER HAPPEN</h3>"
block="<h3>AI BLOCKS HUMAN</h3>"
naive="<h3>AI MADE NAIVE MOVE</h3>"

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
      print "<h3>" + board[0:3] + "<br>\n" + board[3:6] + "<br>\n" + board[6:9] + "</h3>"
      return
   # reset
   elif humaninput == '9':
      board = boardreset
      boardfile = open('board', 'w')
      boardfile.write(boardreset)
      boardfile.close()
      print reset
      print "<h3>" + board[0:3] + "<br>\n" + board[3:6] + "<br>\n" + board[6:9] + "</h3>"
      return
   # occupied
   elif board[int(humaninput)] != humaninput:
   	  print occupied
   	  print "<h3>" + board[0:3] + "<br>\n" + board[3:6] + "<br>\n" + board[6:9] + "</h3>"
   	  return
   else:
      # entered
      board = board.replace(humaninput, 'H')
      boardfile = open('board', 'w')
      boardfile.write(board)
      boardfile.close()
      print entered + humaninput + "</h3>"
      print "<h3>" + board[0:3] + "<br>\n" + board[3:6] + "<br>\n" + board[6:9] + "</h3>"

   # check if human won (should not occur, middle square is always ai A
   if ((re.search(r"HHH......",board)) or 
      (re.search(r"..H..H..H",board)) or 
      (re.search(r"......HHH",board)) or
      (re.search(r"H..H..H..",board))):
      boardfile = open('board', 'w')
      boardfile.write(board)
      boardfile.close()
      print loss
      print "<h3>" + board[0:3] + "<br>\n" + board[3:6] + "<br>\n" + board[6:9] + "</h3>"
      boardfile = open('board', 'w')
      boardfile.write(boardreset)
      boardfile.close()
      board = open('board').read()
      print reset
      print "<h3>" + board[0:3] + "<br>\n" + board[3:6] + "<br>\n" + board[6:9] + "</h3>"
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
   	  print "<h3>" + board[0:3] + "<br>\n" + board[3:6] + "<br>\n" + board[6:9] + "</h3>"
   	  boardfile = open('board', 'w')
   	  boardfile.write(boardreset)
   	  boardfile.close()
   	  board = open('board').read()
   	  print reset
   	  print "<h3>" + board[0:3] + "<br>\n" + board[3:6] + "<br>\n" + board[6:9] + "</h3>"
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
    	print "<h3>" + board[0:3] + "<br>\n" + board[3:6] + "<br>\n" + board[6:9] + "</h3>"
    	boardfile = open('board', 'w')
    	boardfile.write(boardreset)
    	boardfile.close()
    	board = open('board').read()
    	print reset
    	print "<h3>" + board[0:3] + "<br>\n" + board[3:6] + "<br>\n" + board[6:9] + "</h3>"
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
    	print "<h3>" + board[0:3] + "<br>\n" + board[3:6] + "<br>\n" + board[6:9] + "</h3>"
    	# check whether board full
        full=True
        for b in board:
        	if b not in ['A','H']:
        		full=False
        if full == True:
            print draw
            print "<h3>" + board[0:3] + "<br>\n" + board[3:6] + "<br>\n" + board[6:9] + "</h3>"
            boardfile = open('board', 'w')
            boardfile.write(boardreset)
            boardfile.close()
            board = open('board').read()
            print reset
            print "<h3>" + board[0:3] + "<br>\n" + board[3:6] + "<br>\n" + board[6:9] + "</h3>"
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
    	print "<h3>" + board[0:3] + "<br>\n" + board[3:6] + "<br>\n" + board[6:9] + "</h3>"
    	# check whether board full
        full=True
        for b in board:
        	if b not in ['A','H']:
        		full=False
        if full == True:
            print draw
            print "<h3>" + board[0:3] + "<br>\n" + board[3:6] + "<br>\n" + board[6:9] + "</h3>"
            boardfile = open('board', 'w')
            boardfile.write(boardreset)
            boardfile.close()
            board = open('board').read()
            print reset
            print "<h3>" + board[0:3] + "<br>\n" + board[3:6] + "<br>\n" + board[6:9] + "</h3>"
    	return 


print "Content-type: text/html"
print

print """
<html>

<head><title>Tic Tac Toe</title></head>

<body>

  <h3> Tic Tac Toe </h3>
"""

form = cgi.FieldStorage()
position = form.getvalue("position", "(no position)")
print tictactoeboard(position)
print """
  <p>Last Entry: %s</p>
  <p> Note: H is Human and A is AI, In this game, AI should never lose </p>
  <form method="post" action="tictactoe.py">
    <p><h3>Enter position [0-8] or enter 9 to Reset: <input type="text" name="position"/></h3></p>
  </form>

</body>

</html>
""" % position
