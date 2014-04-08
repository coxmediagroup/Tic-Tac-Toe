from django.shortcuts import render

def home(request):
	'The site home page'
	context = {}
	request.session['start'] = True
	return render(request, 'home.html', context)
