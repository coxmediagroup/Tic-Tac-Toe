from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import logging, json

console = logging.getLogger('t3.console')

# Create your views here.
def index(request):
    return render(request, 't3/index.html')
