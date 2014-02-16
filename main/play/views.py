# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response


def home(request):
    return render_to_response('play/home.html',locals())