from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
import json
import random

theBoard = [[' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],[' ']]

def makeMove(board, letter, move):
    board[move] = letter

def isWinner(bo, le):
    return ((bo[7] == le and bo[8] == le and bo[9] == le) or # across the top
    (bo[4] == le and bo[5] == le and bo[6] == le) or # across the middle
    (bo[1] == le and bo[2] == le and bo[3] == le) or # across the bottom
    (bo[7] == le and bo[4] == le and bo[1] == le) or # down the left side
    (bo[8] == le and bo[5] == le and bo[2] == le) or # down the middle
    (bo[9] == le and bo[6] == le and bo[3] == le) or # down the right side
    (bo[7] == le and bo[5] == le and bo[3] == le) or # diagonal
    (bo[9] == le and bo[5] == le and bo[1] == le)) # diagonal

def getBoardCopy(board):
    dupeBoard = []
    for i in board:
        dupeBoard.append(i)
    return dupeBoard

def isSpaceFree(board, move):
    return board[move] == ' '

def chooseRandomMove(board, movesList):
    possibleMoves = []
    for i in movesList:
        if isSpaceFree(board, i):
            possibleMoves.append(i)

    if len(possibleMoves) != 0:
        return random.choice(possibleMoves)
    else:
        return None

def getComputerMove(board):
    computerLetter = 'O'
    playerLetter = 'X'

    # First, check if we can win in the next move
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

    # Try to take the center, if it is free.
    if isSpaceFree(board, 5):
        return 5

    # Try to take one of the corners, if they are free.
    corners = [[1, 9],[3, 7],[7, 3],[9, 1]]
    emptyCorners = []
    for i in corners:
        if not isSpaceFree(board,i[0]):
            try:
                corners.remove([i[1],i[0]])
            except ValueError:
                pass
        else:
            emptyCorners.append(i[0])
    if emptyCorners:
        move = chooseRandomMove(board, emptyCorners)
        if move != None:
            return move

    # Move on one of the sides.
    return chooseRandomMove(board, [2, 4, 6, 8])

def isBoardFull(board):
    for i in range(1, 10):
        if isSpaceFree(board, i):
            return False
    return True

@csrf_exempt
def get_move(request, **kwargs):
    player_move = int(request.POST.get('player_move'))
    game='continue'
    response_data = {}
    if isSpaceFree(theBoard, player_move):
        theBoard[player_move]='X'
        message = ""
        computer_move = ''

        if isBoardFull(theBoard):
            message = 'The game is a tie!'
            game='end'
        else:
            computer_move = getComputerMove(theBoard)
            theBoard[computer_move]='O'
            if isWinner(theBoard, 'O'):
                message = 'The computer has beaten you! You lose.'
                game='end'
            else:
                if isBoardFull(theBoard):
                    message = 'The game is a tie!'
                    game='end'
        response_data['computer_move'] = computer_move

    else:
        message="That place is taken. Move on!"

    response_data['game'] = game
    response_data['message'] = message
    response_data['board'] = theBoard[1:10]
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def IndexView(request):
    for i in range(10):
        theBoard[i]= ' '
    template = loader.get_template('tictactoe.html')
    context = RequestContext(request, {
        'theBoard':theBoard[1:10],
    })
    return HttpResponse(template.render(context))

