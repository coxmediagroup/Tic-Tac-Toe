from django.http import HttpResponse
from django.views.generic import TemplateView

class BoardView(TemplateView):
    template_name = 'board.html'

def home_view(request):
    content = 'Hello World!'
    return HttpResponse(content)

def make_a_move(request):
    return HttpResponse(request.GET['board'], 'json')
