#!/usr/local/bin/python

import random

def startgame():
    #create empty board
    board = [['-','-','-'],
             ['-','-','-'],
             ['-','-','-']]
    #display welcome message and help at start of each game
    print('\nWelcome! I challenge you to a game of Tic-Tac-Toe.')
    displayhelp()
    return board

def displayhelp():
    print('- Each field on the board is assigned to a number (see below):')
    print('                7|8|9')
    print('                4|5|6')
    print('                1|2|3')
    print('- You can only occupy unmarked spaces.')
    print('- The computer will win as soon as he got 3 marks in any row, column or diagonal.')
    print('- It is impossible for you to win (best possible result is a tie).')
    print('- It is easiest to use your NumPad to play the game.\nGood luck!\n')
    
def playerletter():
    #return two letters, first one for human player
    #and second one for computer player
    letter = ''
    print('Would you like to use X or O?')
    letter = raw_input().upper()
    while not (letter == 'X' or letter == 'O'):
        print('Please enter either X or O!')
        letter = raw_input().upper()

    if letter == 'X':
        human = 'X'
        cpu = 'O'
    else:
        human = 'O'
        cpu = 'X'

    return human, cpu

def humanfirst():
    #ask who should go first and return True if human goes first
    #and False if computer goes first
    first = ''
    print('Who should go first: (h) Human or (c) Computer?')
    first = raw_input().lower()
    while not (first == 'h' or first == 'c'):
        print('Please enter either "h" for Human or "c" for Computer!')
        first = raw_input().lower()

    if first == 'h':
        return True
    else:
        return False

def drawboard(board):
    #draw the current board
    print('          ' + board[0][0] + '|' + board[0][1] + '|' + board[0][2])
    print('          ' + board[1][0] + '|' + board[1][1] + '|' + board[1][2])
    print('          ' + board[2][0] + '|' + board[2][1] + '|' + board[2][2])

def isUnoccupied(board,move):
    #test if move was made to unoccupied space
    if (move =='1' and board[2][0] == '-') or (move =='2' and board[2][1] == '-') or (move =='3' and board[2][2] == '-') or (move =='4' and board[1][0] == '-') or(move =='1' and board[2][0] == '-') or(move =='1' and board[2][0] == '-') or(move =='1' and board[2][0] == '-') or(move =='1' and board[2][0] == '-') or(move =='1' and board[2][0] == '-') or(move =='1' and board[2][0] == '-') or(move =='1' and board[2][0] == '-') or(move =='1' and board[2][0] == '-') or(move =='1' and board[2][0] == '-') or(move =='1' and board[2][0] == '-') or(move =='1' and board[2][0] == '-') or(move =='1' and board[2][0] == '-') or(move =='1' and board[2][0] == '-') or(move =='1' and board[2][0] == '-') or(move =='1' and board[2][0] == '-') or(move =='1' and board[2][0] == '-') or(move =='1' and board[2][0] == '-') or(move =='1' and board[2][0] == '-') or(move =='1' and board[2][0] == '-') or (move =='5' and board[1][1] == '-') or (move =='6' and board[1][2] == '-') or (move =='7' and board[0][0] == '-') or (move =='8' and board[0][1] == '-') or (move =='9' and board[0][2] == '-'):
        return True
    else:
        return False

def getUnoccupiedSpaces(board):
    spaces = []
    if board[2][0] =='-':
        spaces.append('1')
    if board[2][1] =='-':
        spaces.append('2')
    if board[2][2] =='-':
        spaces.append('3')
    if board[1][0] =='-':
        spaces.append('4')
    if board[1][1] =='-':
        spaces.append('5')
    if board[1][2] =='-':
        spaces.append('6')
    if board[0][0] =='-':
        spaces.append('7')
    if board[0][1] =='-':
        spaces.append('8')
    if board[0][2] =='-':
        spaces.append('9')
    return spaces

def makemove(b, move, token):
    #function to edit the board according to last move
    if move == '1':
        b[2][0] = token
    if move == '2':
        b[2][1] = token
    if move == '3':
        b[2][2] = token
    if move == '4':
        b[1][0] = token
    if move == '5':
        b[1][1] = token
    if move == '6':
        b[1][2] = token
    if move == '7':
        b[0][0] = token
    if move == '8':
        b[0][1] = token
    if move == '9':
        b[0][2] = token
    return b
    
def makeplayermove(board, token):
    #make players move
    print('Your turn. Where to go next? (enter number for unoccupied space or (h) for help!)')
    move = raw_input()
    free = getUnoccupiedSpaces(board)
    while move not in '1 2 3 4 5 6 7 8 9'.split() or move not in free:
        if move == 'h' or move == 'help':
            displayhelp()
        print('Please enter one of the following numbers for your next move:')
        print(free)
        move = raw_input()
    newboard = makemove(board, move, token)
    return newboard

def getBoardCopy(board):
    from copy import copy
    copBoard = copy(board)
    print(board)
    copBoard[2][0] = 'A'
    print(board)
    print(copBoard)

    return copBoard

def makeAImove(board, token):
    #make AI move based on following priority list:
    #1) make winning move
    #2) block human winning move
    #3) get middle space if first move
    #4) get free corner
    #5) get free side
    
    free = getUnoccupiedSpaces(board)

    #1) make winning move if possible
    for space in free:
        copBoard = getBoardCopy(board)
        copBoard = makemove(copBoard, space, token)
        #check if made move triggers win (or tie?) and return if True
        drawboard(copBoard)

        
    from random import choice
    move = choice(free)
    newboard = makemove(board, move, token)
    return newboard

def win_or_tie(board):
    #check win/tie conditions and print status message
    #return True if no more moves are left or if someone won
    #return False if open moves are left and no one has won
    if board[2][0] == board[2][1] == board[2][2] and board[2][0] is not '-':
        drawboard(board)
        print(board[2][0] + ' wins!')
        return True
    elif board[1][0] == board[1][1] == board[1][2] and board[1][0] is not '-':
        drawboard(board)
        print(board[1][0] + ' wins!')
        return True
    elif board[0][0] == board[0][1] == board[0][2] and board[0][0] is not '-':
        drawboard(board)
        print(board[0][0] + ' wins!')
        return True
    elif board[2][0] == board[1][0] == board[0][0] and board[2][0] is not '-':
        drawboard(board)
        print(board[2][0] + ' wins!')
        return True
    elif board[2][1] == board[1][1] == board[0][1] and board[2][1] is not '-':
        drawboard(board)
        print(board[2][1] + ' wins!')
        return True
    elif board[2][2] == board[1][2] == board[0][2] and board[2][2] is not '-':
        drawboard(board)
        print(board[2][2] + ' wins!')
        return True
    elif board[2][0] == board[1][1] == board[0][2] and board[2][0] is not '-':
        drawboard(board)
        print(board[2][0] + ' wins!')
        return True
    elif board[2][2] == board[1][1] == board[0][0] and board[2][2] is not '-':
        drawboard(board)
        print(board[2][2] + ' wins!')
        return True
    else:
        #check if moves are left and return True if not
        for a in range(0,3):
            for b in range(0,3):
                if board[a][b] == '-':
                    return False
        drawboard(board)
        print('the game ended in a tie!')
        return True

#main
game = True
while game: #game loop until not play again
    tie_or_win = False
    board = startgame()
    letters = playerletter()
    first = humanfirst()
    if first:
        turn = 'human'
    else:
        turn = 'cpu'
        
    while not tie_or_win: #loop until win/tie is True
        if turn == 'human':
            drawboard(board)
            board = makeplayermove(board, letters[0])
            turn = 'cpu'
        else:
            board = makeAImove(board, letters[1])
            turn = 'human'
        tie_or_win = win_or_tie(board)

    print('Do you want to play again? (y/n)')
    answer = raw_input().lower()
    if answer == 'y' or answer == 'yes':
        game = True
    else:
        game = False
