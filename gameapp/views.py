from django.shortcuts import render

def index(request):
   board = getboard("XOXOXOXOX")

   return render(request, 'board.html', {'board': board})

  
def getboard(board_string):
   "Super basic placeholder for getting a board to display to the player"
   board = []
   board.append([list(board_string)[i] for i in range(3)])
   board.append([list(board_string)[i] for i in range(3, 6)])
   board.append([list(board_string)[i] for i in range(6, 9)])
   return board
