from django.template import loader
from django.template.context import RequestContext
from django.http import HttpResponse


def game(request):
    template = loader.get_template('game.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))


def results(request):
    pass