#!/usr/local/bin/python

def startgame():
    #create empty board
    board = [['-','-','-'],
             ['-','-','-'],
             ['-','-','-']]

def playerletter():
    #ask for player letter
    while not (human =='X' or human == 'O'):
        print('Would you like to use X or O?')
        human = input().upper()

def whofirst():
    #ask who should go first
    while not (first == 'h' or first == 'c'):
        print('Who should go first: (h) Human or (c) Computer?')
        first == input()

def drawboard():
    #draw the current board
    print(board[0][0] + '|' + board[0][1] + '|' + board[0][2])
    print(board[1][0] + '|' + board[1][1] + '|' + board[1][2])
    print(board[2][0] + '|' + board[2][1] + '|' + board[2][2])

def getplayermove():
    #get players move

def AImove():
    #get AI move

def win_or_tie():
    #check win/tie conditions
