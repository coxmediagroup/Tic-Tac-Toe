from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext


theBoard = [[' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],[' '],[' ']]

def IndexView(request):
    for i in range(10):
        theBoard[i]= ' '
    template = loader.get_template('tictactoe.html')
    context = RequestContext(request, {
        'theBoard':theBoard[1:10],
    })
    return HttpResponse(template.render(context))

