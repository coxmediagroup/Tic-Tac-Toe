import json
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
import xsos

SIZE = 3
EMPTY = [[0]*SIZE]*SIZE
def default(request):
    if 'xsos_game' not in request.session:
        request.session['xsos_game'] = xsos.Grid(SIZE)
    g = request.session['xsos_game']
    if 'reset' in request.GET:
        g.reset()
        request.session['xsos_game'] = g
        del request.session["player_mark"]
        return HttpResponseRedirect(reverse("default"))
    if 'set_mark' in request.GET and g.grid == EMPTY:
        m = int(request.GET['set_mark'])
        if m in g.marks:
            request.session["player_mark"] = m
    if 'player_mark' in request.session:
        return HttpResponseRedirect(reverse("play"))
    return TemplateResponse(request, 'tictactoe/base.html', {'game':g})

def play(request):
    if 'xsos_game' not in request.session:
        return HttpResponseRedirect(reverse("default"))
    g = request.session['xsos_game']
    mark = request.session["player_mark"]
    if mark == 2 and g.grid == EMPTY:
        move_url = reverse("move") + "?cmp=True"
        return HttpResponseRedirect(move_url)
    # convert grid marks from int to str for the template
    grid = [[g.marks[c] if c else '' for c in r] for r in g.grid]
    return TemplateResponse(request, 'tictactoe/play.html', {'grid': grid, \
        'game':g, 'mark':mark})

def move(request):
    q = request.GET.copy()
    if ('xsos_game' or 'player_mark') not in request.session:
        return HttpResponseRedirect(reverse("default"))
    g = request.session['xsos_game']
    opmark = g._op(int(request.session["player_mark"]))
    if 'cmp' in q:
        g.move(opmark)
        request.session['xsos_game'] = g
        return HttpResponseRedirect(reverse("play"))
    if 'row' not in q or 'col' not in q or 'mark' not in q:
        return HttpResponseBadRequest("Missing parameters")
    r = int(q["row"])
    c = int(q["col"])
    m = int(q["mark"])
    if m in g.marks:
        if not g.grid[r][c]:
            g.grid[r][c] = m
            over, winner = g.game_over()
            if not over:
                g.move(opmark)
            request.session['xsos_game'] = g
            return HttpResponseRedirect(reverse("play"))
    else:
        return HttpResponseBadRequest("Invalid mark")
    