#!/usr/local/bin/python

import random

def startgame():
    #create empty board
    board = [['-','-','-'],
             ['-','-','-'],
             ['-','-','-']]
    #display welcome message and helpmenu help at start of each game
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

def get_token(board, space):
    #return content of board at space
    if space == 1:
        return board[2][0]
    if space == 2:
        return board[2][1]
    if space == 3:
        return board[2][2]
    if space == 4:
        return board[1][0]
    if space == 5:
        return board[1][1]
    if space == 6:
        return board[1][2]
    if space == 7:
        return board[0][0]
    if space == 8:
        return board[0][1]
    if space == 9:
        return board[0][2]

def getUnoccupiedSpaces(board):
    #return list containing all empty spaces (all possible moves)
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
    #add token into the board at move (space)
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
    #ask for humans next turn and make move
    print('Your turn. Where to go next? (enter number for unoccupied space or (h) for help!)')
    move = raw_input()
    free = getUnoccupiedSpaces(board)
    while move not in '1 2 3 4 5 6 7 8 9'.split() or move not in free:
        if move == 'h' or move == 'help':
            displayhelp()
        print('Please enter one of the following numbers for your next move: %s' % free)
        move = raw_input()
    newboard = makemove(board, move, token)
    return newboard

def getBoardCopy(board):
    import copy
    copBoard = copy.deepcopy(board)
    return copBoard

def getForkList(board, mytoken, optoken):
    #create a board to replace mytoken with 1, optoken with 2 and empty spaces with 0
    #find paths on that board where the sum = 1, meaning that these are paths with
    #1 mytoken and 2 empty spaces (one move taken, unblocked by opponent).
    #finally: create one list out of these paths.
    path_list = []
    fork_list = []
    tf = [[0,0,0],[0,0,0],[0,0,0]]
    for row in range(0,3):
        for col in range(0,3):
            if board[row][col] == mytoken:
                tf[row][col] = 1
            elif board[row][col] == optoken:
                tf[row][col] = 2
            #else:
                #continue

    if tf[2][0] + tf[2][1] + tf[2][2] == 1:
        path_list.append([1,2,3])
    if tf[1][0] + tf[1][1] + tf[1][2] == 1:
        path_list.append([4,5,6])
    if tf[0][0] + tf[0][1] + tf[0][2] == 1:
        path_list.append([7,8,9])
    if tf[2][0] + tf[1][0] + tf[0][0] == 1:
        path_list.append([1,4,7])
    if tf[2][1] + tf[1][1] + tf[0][1] == 1:
        path_list.append([2,5,8])
    if tf[2][2] + tf[1][2] + tf[0][2] == 1:
        path_list.append([3,6,9])
    if tf[2][0] + tf[1][1] + tf[0][2] == 1:
        path_list.append([1,5,9])
    if tf[2][2] + tf[1][1] + tf[0][0] == 1:
        path_list.append([3,5,7])

    for path in path_list:
        for space in path:
            fork_list.append(space)
    
    return fork_list

def forkmove(board, mytoken, optoken, bestmove):
    #return best possible move that will create a fork
    #or return list of all possible fork moves (depending
    #on whether bestmove is True or False)
    fork_list = getForkList(board, mytoken, optoken)
    spaces = {}
    for space in fork_list:
        if space not in spaces.keys():
            if mytoken == get_token(board,space):
                continue
            spaces[space] = 0
        else:
            spaces[space] += 1
    
    best = 0
    for number in spaces.keys():
        if spaces[number] > best:
            best = spaces[number]

    forkmove_list = []
    if best > 0:
        for move, number in spaces.iteritems():
            if number == best:
                if bestmove:
                    return str(move)
                elif not bestmove:
                    forkmove_list.append(str(move))
    if not bestmove:
        return forkmove_list
    return None
    
def getForceMoves(board, mytoken, optoken):
    #return all possible moves that would force the opponent
    #to block computer win, thus keeping him from making a fork move
    forklist = getForkList(board, mytoken, optoken)
    forcemoves = []
    for space in forklist:
        if get_token(board, space) != mytoken:
            forcemoves.append(space)
    return forcemoves

def makeAImove(board, letters):
    #make AI move based on following priority list:
    #1) make winning move
    #2) block human winning move
    #3) create fork
    #4) block opposing fork
    #5) take center
    #6) get opposing corner
    #7) take any empty corner
    #8) take any side
    
    free = getUnoccupiedSpaces(board)

    #1) make winning move if possible
    for space in free:
        copBoard = getBoardCopy(board)
        copBoard = makemove(copBoard, space, letters[1])
        winmove = is_win_or_tie(copBoard)
        if winmove:
            move = space
            newboard = makemove(board, move, letters[1])
            return newboard

    #2) block human winning move
    for space in free:
        copBoard = getBoardCopy(board)
        copBoard = makemove(copBoard, space, letters[0])
        winmove = is_win_or_tie(copBoard)
        if winmove:
            move = space
            newboard = makemove(board, move, letters[1])
            return newboard

    #3) make best possible fork move
    move = forkmove(board, letters[1], letters[0], True)
    if move:
        newboard = makemove(board, move, letters[1])
        return newboard

    #4) block opposing fork move
    opfork_list = forkmove(board, letters[0], letters[1], False)
    forkcount = len(opfork_list)
    if forkcount == 1:
        newboard = makemove(board, opfork_list[0], letters[1])
        return newboard
    elif forkcount > 1:
        blockforkmoves = []
        forcemoves = getForceMoves(board, letters[1], letters[0])
        for move in forcemoves:
            copBoard = getBoardCopy(board)
            copBoard = makemove(copBoard, move, letters[1])
            test_opfork_list = forkmove(copBoard, letters[0], letters[1], False)
            for fork in test_opfork_list:
                if fork not in opfork_list:
                    continue
            if str(move) not in opfork_list:
                blockforkmoves.append(move)
        
        if blockforkmoves:
            from random import choice
            move = choice(blockforkmoves)
            newboard = makemove(board, str(move), letters[1])
            return newboard

    #5) take center if open
    if get_token(board, 5) == '-':
        newboard = makemove(board, '5', letters[1])
        return newboard

    #6) take opposite corner
    for corner, opcorner in {'1': 9, '3': 7, '7': 3, '9': 1}.iteritems():
        if get_token(board, int(corner)) == letters[0]:
            if get_token(board, opcorner) == '-':
                newboard = makemove(board, str(opcorner), letters[1])
                return newboard

    
    #7) get free corner
    templist = []
    for space in free:
        if space == '1':
            templist.append(space)
        if space == '3':
            templist.append(space)
        if space == '7':
            templist.append(space)
        if space == '9':
            templist.append(space)
    if templist:
        from random import choice
        cornermove = choice(templist)
        newboard = makemove(board, cornermove, letters[1])
        return newboard

    #8) get free side
    templist = []
    for space in free:
        if space == '2':
            templist.append(space)
        if space == '4':
            templist.append(space)
        if space == '6':
            templist.append(space)
        if space == '8':
            templist.append(space)
    if templist:
        from random import choice
        cornermove = choice(templist)
        newboard = makemove(board, cornermove, letters[1])
        return newboard
            
    move = choice(free)
    newboard = makemove(board, move, letters[1])
    return newboard

def is_win_or_tie(board):
    #check win/tie conditions
    #return True if no more moves are left or if someone won
    #return False if open moves are left and no one has won
    if board[2][0] == board[2][1] == board[2][2] and board[2][0] is not '-':
        return True
    elif board[1][0] == board[1][1] == board[1][2] and board[1][0] is not '-':
        return True
    elif board[0][0] == board[0][1] == board[0][2] and board[0][0] is not '-':
        return True
    elif board[2][0] == board[1][0] == board[0][0] and board[2][0] is not '-':
        return True
    elif board[2][1] == board[1][1] == board[0][1] and board[2][1] is not '-':
        return True
    elif board[2][2] == board[1][2] == board[0][2] and board[2][2] is not '-':
        return True
    elif board[2][0] == board[1][1] == board[0][2] and board[2][0] is not '-':
        return True
    elif board[2][2] == board[1][1] == board[0][0] and board[2][2] is not '-':
        return True
    else:
        #check if moves are left and return True if not
        for a in range(0,3):
            for b in range(0,3):
                if board[a][b] == '-':
                    return False
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
            tie_or_win = is_win_or_tie(board)
            turn = 'cpu'
        else:
            board = makeAImove(board, letters)
            tie_or_win = is_win_or_tie(board)
            turn = 'human'

    drawboard(board)
    print('The game has ended and you did not win!\n')

    print('Do you want to play again? (y/n)')
    answer = raw_input().lower()
    if answer == 'y' or answer == 'yes':
        game = True
    else:
        game = False
