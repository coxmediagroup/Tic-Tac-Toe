from django.shortcuts import render, get_object_or_404
from tic.models import Board
from django.forms.models import model_to_dict




def index(request):
	
	return render(request,'tic/index.html',{})	

def processBoard(request,opick,board):
	mtd=model_to_dict(board)
	if opick:	
		board.opick='o'
		board.save()	
		mtd[opick]='o'
		
	xpick,winners=board.mkPick(mtd)
	mtd[xpick]='x'
	board.xpick='x'
	board.save()		
	myargs={'pk':board.pk,'wingroup':winners,'xpick':xpick}	
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
