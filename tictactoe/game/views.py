from django.shortcuts import render

def game(request):
	
	context = {}
	return render(request, 'game/board.html', context)
