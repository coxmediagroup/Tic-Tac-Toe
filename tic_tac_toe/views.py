from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse('Index')

def make_move(request, row_id, column_id):
    return HttpResponse('Move')
