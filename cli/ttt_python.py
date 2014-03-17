#!/usr/bin/python
import re

noDigits = re.compile('\D')
onlyDigits = re.compile('\d')

gridSize = 3
gameBoard = []

lines = [
                [ 0, 1, 2 ],
                [ 3, 4, 5 ],
                [ 6, 7, 8 ],
                [ 0, 3, 6 ],
                [ 1, 4, 7 ],
                [ 2, 5, 8 ],
                [ 0, 4, 8 ],
                [ 2, 4, 6 ]
            ]

bestLocs = [4, 8, 6, 2, 0, 7, 5, 3, 1]

def init():
    count = 1
    tempBoard = []
    for loc in range(0,(gridSize**2)):
        tempBoard.append(" ")
        count +=1
    return tempBoard

def printBoard(lastPrint):
    print "+---+---+---+"
    for loc in range(0,(gridSize**2)):
        if lastPrint!=0:
            if onlyDigits.match(gameBoard[loc]):
                print "|   " ,
            if noDigits.match(gameBoard[loc]):
                print "| " + str(gameBoard[loc]),
        else:
            if str(gameBoard[loc]) == " ":
                print "| " + str(int(loc+1)),
            else:
                print "| " + str(gameBoard[loc]),
        if (loc+1) % gridSize == 0:
            print "|\n+---+---+---+"

def checkBoard():
    for line in lines:
        sum = 0
        openLoc = 0
        for loc in line:
            if gameBoard[loc] == 'X':
                sum += 1
            elif gameBoard[loc] == 'O':
                sum += -1
            else:
                openLoc = loc
        if sum==3:
            print "X Wins!\n"
            printBoard(1)
            exit(0)
        elif sum == -3:
            print "O Wins!\n"
            printBoard(1)
            exit(0)
    for loc in gameBoard:
        if loc==" ":
            return 0
    print "TIE!\n"
    printBoard(1)
    exit(0)

def getNextMove():
    for line in (lines):
        sum = 0
        openLoc = -1
        for loc in (line):
            if(gameBoard[loc] == 'X'):
                sum += 1
            elif(gameBoard[loc] == 'O'):
                sum += -1
            else:
                openLoc = loc

        if(sum == -2 and openLoc >= 0):
            gameBoard[openLoc]='O'
            return 0
    for line in (lines):
        sum = 0
        openLoc = -1
        for loc in (line):
            if(gameBoard[loc] == 'X'):
                sum += 1
            elif(gameBoard[loc] == 'O'):
                sum += -1
            else:
                openLoc = loc
        if(sum == 2 and openLoc >= 0):
            gameBoard[openLoc]='O'
            return 0
    for line in ((lines[6], lines[7])):
        sum = 0
        openLoc = -1
        for loc in (line):
            if(gameBoard[loc] == 'X'):
                sum += 1
            elif(gameBoard[loc] == 'O'):
                sum += -1
            else:
                openLoc = loc
        if(sum == 0 and openLoc >= 0):
            gameBoard[openLoc]='O'
            return 0
    for bestLoc in (bestLocs):
        if onlyDigits.match(gameBoard[bestLoc]):
            gameBoard[bestLoc]='O'
            return 0



gameBoard = init()

printBoard(0)

while(1):
    location = raw_input( "Place your 'X': ")
    if location.isdigit():
        location = int(location)
        if location>0 and location<=9:
            element = gameBoard[location-1]
            if element == " ":
                gameBoard[location-1] = 'X'
                if not checkBoard():
                    getNextMove()
            else:
                print "Bad move.\n"
            printBoard(0)
        checkBoard()

