from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext, loader

def index(request):
	template = loader.get_template('gameinterface/index.html')
	context = RequestContext(request, {})
	return HttpResponse(template.render(context))
