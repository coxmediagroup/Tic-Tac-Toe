# session is used to persist the positions taken, and the number of turns
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.template import Context, loader
import pdb

def play(request):
	request.session[int (request.POST['position'])] = 2 
	request.session['count'] += 1
	if request.session['count'] == 1: #first turn
		if request.POST['position'] in ['4','5','7']:
			responsePosition = 2
		if request.POST['position'] in ['2','3']:
			responsePosition = 4
		if request.POST['position'] in ['8','9']:
			responsePosition = 3
		if request.POST['position'] in ['6']:
			responsePosition = 5
		
	if request.session['count'] == 2: #second turn
		if request.session[2] == 1:
			if request.POST['position'] <> '3':
				responsePosition = 3
			elif request.session[5] <> 2:
				responsePosition = 5
			else:
				responsePosition = 7
		if request.session[4] == 1:
			if request.POST['position'] <> '7':
				responsePosition = 7
			else:
				responsePosition = 5
		if request.session[3] == 1:
			if request.POST['position'] <> '2':
				responsePosition = 2
			else:
				responsePosition = 5
		if request.session[5] == 1:
			if request.POST['position'] <> '9':
				responsePosition = 9
			else:
				responsePosition = 3
		
	if request.session['count'] == 3: #third turn
		if request.session[2] == 1 and request.session[5] == 1:
			if request.POST['position'] <> '8':
				responsePosition = 8
			else:
				responsePosition = 9
		else:
			if request.POST['position'] <> '4':
				responsePosition = 4
			else:
				responsePosition = 6
			
		if request.session[4] == 1 and request.session[5] == 1:
			if request.POST['position'] <> '6':
				responsePosition = 6
			else:
				responsePosition = 8
		if request.session[3] == 1 and request.session[5] == 1:
			if request.POST['position'] <> '7':
				responsePosition = 7
			elif request.session[8] == 2:
				responsePosition = 9
			else:
				responsePosition = 8
		if request.session[5] == 1 and request.session[3] == 1:
			if request.POST['position'] <> '2':
				responsePosition = 2
			else:
				responsePosition = 7
		

	request.session[responsePosition] = 1
		
	response_dict = {
		'position': responsePosition
	}	
	return render_to_response('position.html', response_dict, context_instance=RequestContext(request))

def start(request):
	request.session.flush()
	request.session[1] = 1 # 1 indicate taken by machine, 2 by opponent, 0 not taken yet
	for i in range(2,9):
		request.session[i] = 0
	request.session['count'] = 0 # count the number of turns
	response_dict = {
	}	
	return render_to_response('index.html', response_dict, context_instance=RequestContext(request))
