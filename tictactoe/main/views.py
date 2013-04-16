from django.http import HttpResponse
from django.template import Context, loader

def index(request):
    template = loader.get_template('main/index.html')
    # Leaving like this for now... deciding whether necessary.
    context = Context({})
    return HttpResponse(template.render(context))
