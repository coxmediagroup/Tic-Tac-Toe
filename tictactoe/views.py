import json
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
import xsos

def default(request):
    if 'xsos_game' not in request.session:
        request.session['xsos_game'] = xsos.Grid()
    g = request.session['xsos_game']
    if 'player_mark' not in request.session:
        pass
    return TemplateResponse(request, 'tictactoe/base.html', {'game':g})

def play(request):
    if 'xsos_game' not in request.session:
        request.session['xsos_game'] = xsos.Grid()
    g = request.session['xsos_game']
    mark = 1
    grid = '<table>'
    size = g.size
    for r in range(size):
        grid += "<tr>" 
        for c in range(size):
            grid += "<td>"
            cell_mark = g.grid[r][c]
            if g.grid[r][c]:
                grid += g.marks[cell_mark]
            else:
                grid += '<a href="' + reverse("move") + '?row=' + str(r) + \
                "&col=" + str(c) + "&mark="+ str(mark) +'">_</a>'
            grid += "</td>"
        grid += "</tr>"    
    grid += "</table>"
    return TemplateResponse(request, 'tictactoe/play.html', {'grid': grid, \
        'game':g})

def move(request):
    q = request.GET.copy()
    if 'xsos_game' not in request.session:
        return HttpResponseBadRequest("Game not initialized")
    if 'row' not in q or 'col' not in q or 'mark' not in q:
        return HttpResponseBadRequest("Missing parameters")
    g = request.session['xsos_game']
    r = int(q["row"])
    c = int(q["col"])
    m = int(q["mark"])
    if m in g.marks:
        if not g.grid[r][c]:
            g.grid[r][c] = m
            request.session['xsos_game'] = g
            return HttpResponseRedirect(reverse("play"))
    else:
        return HttpResponseBadRequest("Invalid mark")
    