# Python2

import os
import time

def setupBoard():
    board = [
            ['1','2','3'],
            ['4','5','6'],
            ['7','8','9']
            ]

    return board

def printBoard(board):
    os.system('cls' if os.name == 'nt' else 'clear')
    print "\n"
    print board[0]
    print board[1]
    print board[2]
    print "\n"


def playerTurn(board):
    validInput = False
    while validInput == False:
        userInput = raw_input("Enter a square: ")

        row = 0
        col = 0
        for line in board:
            try:
                col = line.index(userInput)

                line[col] = 'X'

                validInput = True
            except:
                if row==2:
                    print "Please enter a valid square."
                    validInput = False
                else:
                    row+=1

def checkWin(board):
    #Check horizontal wins
    if ((board[0][0]==board[0][1] and board[0][1]==board[0][2]) or
        (board[1][0]==board[1][1] and board[1][1]==board[1][2]) or
        (board[2][0]==board[2][1] and board[2][1]==board[2][2])):
        return True
    #Check vertical wins
    if ((board[0][0]==board[1][0] and board[1][0]==board[2][0]) or
        (board[0][1]==board[1][1] and board[1][1]==board[2][1]) or
        (board[0][2]==board[1][2] and board[1][2]==board[2][2])):
        return True
    #Check diagonal wins
    if ((board[0][0]==board[1][1] and board[1][1]==board[2][2]) or
        (board[2][0]==board[1][1] and board[1][1]==board[0][2])):
        return True
    return False

def checkCat(board):
    #Check to see if the board has any numbers remaining.
    if ((board[0].count('1') == 0 and board[0].count('2') == 0 and board[0].count('3') == 0) and
        (board[1].count('4') == 0 and board[1].count('5') == 0 and board[1].count('6') == 0) and
        (board[2].count('7') == 0 and board[2].count('8') == 0 and board[2].count('9') == 0)):
        return True
    return False

def aiTurn(board):
    validMove = False
    for line in board:
        #Check for horizontal win or block
        if ((line.count('O') == 2 and line.count('X') == 0) or
            (line.count('X') == 2 and line.count('O') == 0)):
            col = 0
            for item in line:
                if item != 'X' and item != 'O' and validMove == False:
                    line[col] = 'O'
                    validMove = True
                col+=1
    diag = []
    diag.append(board[0][0])
    diag.append(board[1][1])
    diag.append(board[2][2])

    #Check for diagonal win or block
    if ((diag.count('O') == 2 and diag.count('X') == 0) or
        (diag.count('X') == 2 and diag.count('O') == 0)):
        col = 0
        for item in diag:
            if item != 'O' and item != 'X' and validMove == False:
                board[col][col] = 'O'
                validMove = True
            col+=1

    rotatedBoard=zip(*board[::-1])
    rotatedBoard=[list(line) for line in rotatedBoard]
    #Check for vertical win or block
    for line in rotatedBoard:
        if ((line.count('O') == 2 and line.count('X') == 0) or
            (line.count('X') == 2 and line.count('O') == 0)):
            col = 0
            for item in line:
                if item != 'X' and item != 'O' and validMove == False:
                    line[col] = 'O'
                    validMove = True
                col+=1

    diag = []
    diag.append(rotatedBoard[0][0])
    diag.append(rotatedBoard[1][1])
    diag.append(rotatedBoard[2][2])

    #Check for other diagonal win or block
    if ((diag.count('O') == 2 and diag.count('X') == 0) or
        (diag.count('X') == 2 and diag.count('O') == 0)):
        col = 0
        for item in diag:
            if item != 'O' and item != 'X' and validMove == False:
                rotatedBoard[col][col] = 'O'
                validMove = True
            col+=1

    board=zip(*rotatedBoard)[::-1]
    board=[list(line) for line in board]

    #If no win/block, then center, corners, sides, in that order of availability
    if validMove == False:
        if board[1][1] == '5':
            board[1][1] = 'O'
            validMove = True
        elif board[0][0] == '1':
            board[0][0] = 'O'
            validMove = True
        elif board[0][2] == '3':
            board[0][2] = 'O'
            validMove = True
        elif board[2][0] == '7':
            board[2][0] = 'O'
            validMove = True
        elif board[2][2] == '9':
            board[2][2] = 'O'
            validMove = True
        elif board[0][1] == '2':
            board[0][1] = 'O'
            validMove = True
        elif board[1][0] == '4':
            board[1][0] = 'O'
            validMove = True
        elif board[1][2] == '6':
            board[1][2] = 'O'
            validMove = True
        elif board[2][1] == '8':
            board[2][1] = 'O'
            validMove = True

    return board

board = setupBoard()

while checkWin(board) == False and checkCat(board) == False:
    printBoard(board)
    print "Player Turn"
    playerTurn(board)

    printBoard(board)

    if checkWin(board) == False and checkCat(board) == False:
        board = aiTurn(board)
        printBoard(board)
        print "Computer Turn"
        time.sleep(2)

if checkWin(board) == True:
    print "Winner"
elif checkCat(board) == True:
    print "Cat Game"
