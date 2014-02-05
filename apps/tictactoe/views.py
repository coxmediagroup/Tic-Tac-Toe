# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, loader

def greetings(request):
    t = loader.get_template("tictactoe/tictactoe.html")
    return HttpResponse(t.render(RequestContext(request,{'gridwidth':50,'use_site_header':True})))

def result(request):
    return HttpResponse("1");
