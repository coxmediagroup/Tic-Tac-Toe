from django.shortcuts import render, get_object_or_404
from tic.forms import TicBoardForm
from tic.models import TicBoard
from django.forms.models import model_to_dict


def index(request):
	return render(request,'tic/index.html',{})	


def createBoard(request):
	ticboard=TicBoard()
	ticboard.save()
	myargs=processBoard(request,False,ticboard)

	return render(request,'tic/tic.js',myargs)	


def updateBoard(request,pk,opick):
	ticboard=get_object_or_404(TicBoard, pk=pk)
	myargs=processBoard(request,opick,ticboard)

	return render(request,'tic/tic.js',myargs)	



def processBoard(request,opick,ticboard):
	mtd=model_to_dict(ticboard)
	if opick:		
		mtd[opick]='o'
	form=TicBoardForm()
	xpick,winners=form.mkPick(mtd)
	mtd[xpick]='x'
	form =TicBoardForm(mtd, instance=ticboard)			
	if form.is_valid():
		board=form.save()	
		board.save()		
	myargs={'pk':board.pk,'wingroup':winners,'xpick':xpick,'form':form}	

	return myargs
	

