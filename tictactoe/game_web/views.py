# game_web views.py
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext

def index(request):
    return render_to_response('commercial/home.html', context_instance = RequestContext(request))