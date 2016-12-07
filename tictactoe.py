#!/usr/bin/python


####################################################################################
#                                                                                  #
# "Create a Tic Tac Toe game that can interactively play the game and never lose." #
#                                                                                  #
# Tic Tac Toe is a zero sum game, where one side's loss is the other's gain. If    #    
# the human player plays the game intelligently the game always ends up in a draw. #
#                                                                                  # 
#  --Aldrich                                                                       #
####################################################################################

import random

def drawBoard(board):
    # This function prints out the board.
    print('   |   |')
    print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
    print('   |   |')

def inputPlayerLetter():
    # This function the player choose between 'X' or 'O'.
    letter = ''
    while not (letter == 'X' or letter == 'O'):
        print('Do you want to be X or O?')
        letter = raw_input().upper()

    # the first element in the list is the player's letter, the second is the computer's letter.
    if letter == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']

def whoGoesFirst():
    # This function randomly choose the player who goes first.
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'

def playAgain():
    # This function returns True if the player enters yes or y.
    print('Do you want to play again? (yes or no)')
    return raw_input().lower().startswith('y')

def makeMove(board, letter, move):
    board[move] = letter

def isWinner(boa, let):
    # Given a board and a player's letter, this function returns True if that player has won.
    #Winning combinations:
    return ((boa[7] == let and boa[8] == let and boa[9] == let) or # across the top
    (boa[4] == let and boa[5] == let and boa[6] == let) or # across the middle
    (boa[1] == let and boa[2] == let and boa[3] == let) or # across the bottom
    (boa[7] == let and boa[4] == let and boa[1] == let) or # down the left side
    (boa[8] == let and boa[5] == let and boa[2] == let) or # down the middle
    (boa[9] == let and boa[6] == let and boa[3] == let) or # down the right side
    (boa[7] == let and boa[5] == let and boa[3] == let) or # diagonal
    (boa[9] == let and boa[5] == let and boa[1] == let)) # diagonal

def getBoardCopy(board):
    # This function makes a duplicate of the board list.
    dupeBoard = []

    for i in board:
        dupeBoard.append(i)

    return dupeBoard

def isSpaceFree(board, move):
    # Return true if the move is free on the board.
    return board[move] == ' '

def getPlayerMove(board):
    # This function lets the player type in his move.
    move = ' '
    while move not in '1 2 3 4 5 6 7 8 9'.split() or not isSpaceFree(board, int(move)):
        print('What is your next move? (1-9)')
        move = raw_input()
    return int(move)

def chooseRandomMoveFromList(board, movesList):
    # Returns a valid move from the list on the board.
    # Returns None if there is no valid move.
    possibleMoves = []
    for i in movesList:
        if isSpaceFree(board, i):
            possibleMoves.append(i)

    if len(possibleMoves) != 0:
        return random.choice(possibleMoves)
    else:
        return None

def getComputerMove(board, computerLetter):
    # Given a board and the computer's letter, determine where to move and return that move.
    if computerLetter == 'X':
        playerLetter = 'O'
    else:
        playerLetter = 'X'

    ##############################################################
    #                  AI Algorithm                              #   
    #                                                            #
    # 1. Check if it's a winning move then make the move         #
    # 2. If the human player will win on the next move block him #
    # 3. Always take the corners if they are free                #
    # 4. Always take the center if it is free                    #
    #                                                            #
    ##############################################################

    # First, check if AI can win in the next move
    for i in range(1, 10):
        copy = getBoardCopy(board)
        if isSpaceFree(copy, i):
            makeMove(copy, computerLetter, i)
            if isWinner(copy, computerLetter):
                return i

    # Check if the player could win on his next move, and block them.
    for i in range(1, 10):
        copy = getBoardCopy(board)
        if isSpaceFree(copy, i):
            makeMove(copy, playerLetter, i)
            if isWinner(copy, playerLetter):
                return i

    # Try to take one of the corners, if they are free.
    move = chooseRandomMoveFromList(board, [1, 3, 7, 9])
    if move != None:
        return move

    # Try to take the center, if it is free.
    if isSpaceFree(board, 5):
        return 5

    # Move on one of the sides.
    return chooseRandomMoveFromList(board, [2, 4, 6, 8])

def isBoardFull(board):
    # This function returns True if every space on the board has been taken. 
    for i in range(1, 10):
        if isSpaceFree(board, i):
            return False
    return True


print('Let''s Play Tic Tac Toe!')

while True:
    # Reset the board
    theBoard = [' '] * 10
    playerLetter, computerLetter = inputPlayerLetter()
    turn = whoGoesFirst()
    print('The ' + turn + ' will go first.')
    gameIsPlaying = True

    while gameIsPlaying:
        if turn == 'player':
            # Player's turn.
            drawBoard(theBoard)
            move = getPlayerMove(theBoard)
            makeMove(theBoard, playerLetter, move)

            if isWinner(theBoard, playerLetter):
                drawBoard(theBoard)
                print('The human player won the game!')
                gameIsPlaying = False
            else:
                if isBoardFull(theBoard):
                    drawBoard(theBoard)
                    print('This game is a draw!')
                    break
                else:
                    turn = 'computer'

        else:
            # Computer's turn.
            move = getComputerMove(theBoard, computerLetter)
            makeMove(theBoard, computerLetter, move)

            if isWinner(theBoard, computerLetter):
                drawBoard(theBoard)
                print('The computer won the game!')
                gameIsPlaying = False
            else:
                if isBoardFull(theBoard):
                    drawBoard(theBoard)
                    print('This game is a draw!')
                    break
                else:
                    turn = 'player'

    if not playAgain():
        break

