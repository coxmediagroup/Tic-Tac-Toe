#!/bin/python
import sys
from tictactoe.board import Board
from tictactoe.ai import AI

def play():
    b=Board()
    ai=AI('o',AI.moveAI)
    while not b.isFilled():
        print str(b) + '\nPlease input a number representing the space '\
          'you want to mark in the range 0-8, then press enter: '
        msg = sys.stdin.readline()
        try:
            location=int(msg)
            if b.isMarked(location):
                print('Please choose a space that has not already been filled in')
                continue
            b.mark(location, 'x')
            if b.isWinner('x'):
                print('X wins!')
                return
            if not b.isFilled():
                ai.turn(b)
                if b.isWinner('o'):
                    print('O wins!')
                    return
        except:
           print('Please input a valid number between 0-8')
    print('Stalemate, please play again!')
    
if __name__ == '__main__':
    print "Welcome to tic-tac-toe, where we offer nothing less than the "\
      "most straightforward experience you\'ve ever had"
    while True:
        play()