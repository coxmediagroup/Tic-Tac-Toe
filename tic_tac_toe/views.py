import json

from django.core.cache import cache
from django.http import HttpResponse
from django.template import RequestContext, loader

# Just one static view
def index(request):
    template = loader.get_template('tic_tac_toe/index.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

# Process AI turn (to prevent player from being able to cheat)
def ai(request):
    data = None
    valid = True
    differences = 0
    squares = json.loads(request.POST["squares"])

    if (cache.get('squares') == None):
        cache.set('squares', squares, 600)
        differences = 1
    else:
        old_squares = cache.get('squares')
        for index in range(9):
            if (old_squares[index] == "") and (squares[index] != old_squares[index]):
                differences = differences + 1
            elif (old_squares[index] != squares[index]):
                valid = False
                break
        if (differences > 1):
            valid = False

    if not valid:
        data = {"success": False, "move_index": -1}
    elif (differences == 0):
        data = {"success": True, "move_index": -1}
    else:
        index = 0
        squares[index] = "O"
        cache.set('squares', squares, 600)
        data = {"success": True, "move_index": 0}

    return HttpResponse(json.dumps(data), content_type="application/json", status=200)

def new(request):
    cache.set('squares', None, 10)
    data = {"success": True}
    return HttpResponse(json.dumps(data), content_type="application/json", status=200)
