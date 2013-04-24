from django.shortcuts import render


def index(request):
    render(request, 'homepage/index.html')