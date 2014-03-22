from django.shortcuts import render_to_response

def standard(request):
    o = dict(test='you suck')
    return render_to_response('grid.html', 0)