from django.shortcuts import render
from django.http import HttpResponse
import json

# Create your views here.

def index(http_request):
  return HttpResponse("hello there")
