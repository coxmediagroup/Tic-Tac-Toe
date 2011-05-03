#!/usr/local/bin/python

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
    print('7|8|9')
    print('4|5|6')
    print('1|2|3')
    print('- You can only occupy unmarked spaces.')
    print('- The computer will win as soon as he got 3 marks in any row, column or diagonal.')
    print('- It is impossible for you to win (best possible result is a tie).')
    print('- It is easiest to use your NumPad to play the game.\nGood luck!\n')
    
def playerletter():
    #ask for player letter
    human = ''
    print('Would you like to use X or O?')
    human = raw_input().upper()
    while not (human == 'X' or human == 'O'):   
        print('Please enter either X or O!')
        human = raw_input().upper()
    return human

def whofirst():
    #ask who should go first
    first = ''
    print('Who should go first: (h) Human or (c) Computer?')
    first = raw_input().lower()
    while not (first == 'h' or first == 'c'):
        print('Please enter either h for Human or c for Computer!')
        first = raw_input().lower()
    return first

def drawboard():
    #draw the current board
    print(board[0][0] + '|' + board[0][1] + '|' + board[0][2])
    print(board[1][0] + '|' + board[1][1] + '|' + board[1][2])
    print(board[2][0] + '|' + board[2][1] + '|' + board[2][2])

def isUnoccupied(board,move):
    #test if move was made to unoccupied space
    if (move =='1' and board[2][0] == '-') or (move =='2' and board[2][1] == '-') or (move =='3' and board[2][2] == '-') or (move =='4' and board[1][0] == '-') or(move =='1' and board[2][0] == '-') or(move =='1' and board[2][0] == '-') or(move =='1' and board[2][0] == '-') or(move =='1' and board[2][0] == '-') or(move =='1' and board[2][0] == '-') or(move =='1' and board[2][0] == '-') or(move =='1' and board[2][0] == '-') or(move =='1' and board[2][0] == '-') or(move =='1' and board[2][0] == '-') or(move =='1' and board[2][0] == '-') or(move =='1' and board[2][0] == '-') or(move =='1' and board[2][0] == '-') or(move =='1' and board[2][0] == '-') or(move =='1' and board[2][0] == '-') or(move =='1' and board[2][0] == '-') or(move =='1' and board[2][0] == '-') or(move =='1' and board[2][0] == '-') or(move =='1' and board[2][0] == '-') or(move =='1' and board[2][0] == '-') or (move =='5' and board[1][1] == '-') or (move =='6' and board[1][2] == '-') or (move =='7' and board[0][0] == '-') or (move =='8' and board[0][1] == '-') or (move =='9' and board[0][2] == '-'):
        return True
    else:
        return False

def getplayermove(board):
    #get players move
    print('Your turn. Where to go next? (enter number for unoccupied space or (h) for help!')
    move = input()
    while move not in '1 2 3 4 5 6 7 8 9'.split():
        print('Not a number. Please enter a number 1-9 for your next move.')
        move = input()
        #test if user requested help
    #if (move == 'h') or (move =='help'):
     #       displayhelp()
        #test if chosen move is valid
            

def AImove():
    #get AI move
    print('AI')

def win_or_tie():
    #check win/tie conditions
    print('WIN')

#main
game = startgame()
pletter = playerletter()
first = whofirst()
