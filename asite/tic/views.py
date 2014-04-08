from django.shortcuts import render, get_object_or_404
from tic.models import Board
from django.forms.models import model_to_dict




def index(request):
	
	return render(request,'tic/index.html',{})
	
def dict_to_board(mtd,board):
	board=Board(**mtd) 
	board.save()
	return board	
	
def setPick(pick,val,mtd,board):
	mtd[pick]=val
	board=dict_to_board(mtd,board)
	return board			

def processBoard(request,opick,board):

	mtd=model_to_dict(board)
	
	if opick:
		board=set_pick(opick,'o',mtd,board)		
	
	xpick,winners=board.mkPick(mtd)
	
	board=set_pick(xpick,'x',mtd,board)
	
	myargs={'pk':board.pk,'wingroup':winners,'xpick':xpick,'mtd':mtd}	
	return myargs
	



def createBoard(request):
	board=Board()
	board.save()
	myargs=processBoard(request,False,board)
	return render(request,'tic/tic.js',myargs)	



def updateBoard(request,pk,opick):
	
	board=get_object_or_404(Board, pk=pk)
	myargs=processBoard(request,opick,board)
	return render(request,'tic/tic.js',myargs)	
