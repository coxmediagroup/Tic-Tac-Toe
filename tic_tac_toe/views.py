from django.http import HttpResponse
from django.template import RequestContext, loader

# Just one static view
def index(request):
    template = loader.get_template('tic_tac_toe/index.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))
