from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
# Create your views here.
import re

noDigits = re.compile('\D')
onlyDigits = re.compile('\d')
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

def index(request):
    gameBoard = []
    information = ""
    gameOn = 1;
    firstPlay = 1;
    if request.method == 'POST':
        firstPlay = 0;
        for element in range(0,9):
            if int(request.POST.get("chosenLoc", "")) == element:
                gameBoard.append("X")
            else:
                gameBoard.append(request.POST.get("loc" + str(element), ""))
        result = checkBoard(gameBoard)
        if(result == 0):
            gameBoard = getNextMove(gameBoard)
            result = checkBoard(gameBoard)
            if(result != 0):
                information = result
                gameOn = 0
        else:
            information = result
            gameOn = 0
    else:
        for element in range(0,9):
            gameBoard.append(" ")
    t = loader.get_template('board/index.html')
    c = RequestContext(request,{'gameBoard': gameBoard, "information":information, "gameOn":gameOn, 'firstPlay':firstPlay});
    return HttpResponse(t.render(c))

def checkBoard(gameBoard):
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
            return "X wins"
        elif sum == -3:
            return "O wins"
    for loc in gameBoard:
        if loc==" ":
            return 0
    return "Tie!"

def getNextMove(gameBoard):
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
            return gameBoard
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
            return gameBoard
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
        if((sum == 0 or sum == 1) and openLoc >= 0):
            gameBoard[openLoc]='O'
            return gameBoard
    for bestLoc in (bestLocs):
        if gameBoard[bestLoc]==" ":
            gameBoard[bestLoc]='O'
            return gameBoard
