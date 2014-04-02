from django.shortcuts import render
from tic.forms import TicBoardForm

def play(request):

	if request.method == 'POST':
		rp=request.POST.copy()
		f = TicBoardForm(request.POST)
		pick,winners=f.mkPick(rp)
		if f.is_valid():
			pass	
				
		return render(request,'tic/ticboard_form.html',{'form':f,'pick':pick,'wingroup':winners})	

	else:
		f=TicBoardForm()
		freshboard=1
		
		if f.is_valid():
			pass	
				
		
		return render(request,'tic/ticboard_form.html',{'form':f,'freshboard':1})	


