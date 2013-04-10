from django.http import HttpResponse

def index(request):
    return HttpResponse("Tic Tac Toe enabled.")
