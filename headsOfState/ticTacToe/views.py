#project/app/views.py
from django.shortcuts import render_to_response


def mainPage(request):
    return render_to_response('index.html') 






