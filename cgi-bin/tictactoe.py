# tic tac toe game where AI never loses
# Ravi Basawa as part of Cox Communications Radio test assignment
# assumption: AI takes first move
# algorithm: a comprehensive state transition table deemed 
#            practical because the above assumption and the
#            characteristic board symmetry reduces the size
#            of the table to manageable and intellible level
# initial stage - naive tic tac toe

import sys
import os 
import time 
import re

board=""
strategy="naive" # for testing
# strategy="intelligent"  # use this one
boardreset="0123A5678"
losestates=[]
winstates=[]
drawstates=[]
rules=[]

validhumaninput=["0","1","2","3","4","5","6","7","8","9"]

result=""
invalid="INPUT NEEDS TO BE IN RANGE 0..8 TO MARK BOARD OR 9 TO RESET BOARD"
reset="GAME RESET"
occupied="SQUARE ALREADY FILLED, NO ENTRY MADE"
entered="HUMAN 'H' ENTERED SUCCESFULLY INTO SQUARE "
win="AI WINS GAME, RESET WITH 9 TO PLAY AGAIN"
draw="AI DRAWS GAME, RESET WITH 9 TO PLAY AGAIN"
loss="AI LOSES GAME, SHOULD NEVER HAPPEN, RESET WITH 9 TO PLAY AGAIN"


def tictactoeboard(humaninput):

   # create board if absent
   if not os.path.exists('board'):
      boardfile = open('board', 'w')
      boardfile.write(boardreset)
      boardfile.close()

   # create rules if absent
   # rules = getrules()
   # read board from file
   board = open('board').read()
   
   # if invalid
   if humaninput not in validhumaninput:
      print board[0:3] + "\n" + board[3:6] + "\n" + board[6:9]
      print invalid
      return

   # game reset
   if humaninput == '9':
      board = boardreset
      boardfile = open('board', 'w')
      boardfile.write(boardreset)
      boardfile.close()
      print board[0:3] + "\n" + board[3:6] + "\n" + board[6:9]
      print reset
      return

   # if occupied
   if board[int(humaninput)] != humaninput:
      print board[0:3] + "\n" + board[3:6] + "\n" + board[6:9]
      print occupied
      return

   # write to board
   board = board.replace(humaninput, 'H')
   boardfile = open('board', 'w')
   boardfile.write(board)
   boardfile.close()

   # check if ai loss
   if ((re.search(r"HHH......",board)) or 
      (re.search(r"..H..H..H",board)) or 
      (re.search(r"......HHH",board)) or
      (re.search(r"H..H..H..",board))):
      print board[0:3] + "\n" + board[3:6] + "\n" + board[6:9]
      # reset board
      board = boardreset
      boardfile = open('board', 'w')
      boardfile.write(boardreset)
      boardfile.close()
      print loss
      return

   # check if board full for draw
   full=True
   for b in board:
      if b not in ['A','H']:
         full=False
   if full:
      print board[0:3] + "\n" + board[3:6] + "\n" + board[6:9]
      # reset board
      board = boardreset
      boardfile = open('board', 'w')
      boardfile.write(boardreset)
      boardfile.close()
      print draw
      return

   # have AI write to board naively
   for bi in range(len(board)):
      if board[bi] not in ['A','H']:
      	 board = board.replace(str(bi), 'A')
      	 break

    # change to have AI write to board intelligently

   # check whether board is an ai win
   if ((re.search(r"AAA......",board)) or 
      (re.search(r"..A..A..A",board)) or
      (re.search(r"......AAA",board)) or
      (re.search(r"A..A..A..",board)) or
      (re.search(r"A...A...A",board)) or
      (re.search(r"..A.A.A..",board))):
      print board[0:3] + "\n" + board[3:6] + "\n" + board[6:9]
      # reset board
      board = boardreset
      boardfile = open('board', 'w')
      boardfile.write(boardreset)
      boardfile.close()
      print win
      return

   # check whether board full
   full=True
   for b in board:
      if b not in ['A','H']:
         full=False
   if full:
      print board[0:3] + "\n" + board[3:6] + "\n" + board[6:9]
      # reset board
      board = boardreset
      boardfile = open('board', 'w')
      boardfile.write(boardreset)
      boardfile.close()
      print draw
      return

   # update file from board then return
   print board[0:3] + "\n" + board[3:6] + "\n" + board[6:9]
   boardfile = open('board', 'w')
   boardfile.write(board)
   boardfile.close()
   return


# def getrules():
#   rules.insert('0123A5678,')

# test tictactoeboard
   
# 0..8 : Mark Board ('H')
# 9    : Reset Board
myhumaninput = '9'
print tictactoeboard(myhumaninput)

#print tictactoeboard('2')
#print tictactoeboard('9')
#print tictactoeboard('7')


