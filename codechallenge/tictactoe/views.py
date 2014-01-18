
import sys

from django.shortcuts import render_to_response
from django.template import RequestContext

from .engine import GameEngine

def index(request):
    return render_to_response('tictactoe/index.html', context_instance=RequestContext(request))

def normal_game(request):
    """ Normal game """
    # context for tempate
    context = { }

    if not 'game' in request.session:
        # construct a game engine
        game = GameEngine()

    else:
        # load game engine from session
        game = GameEngine.from_dict(request.session['game']) 

    if request.method == 'POST':
        action = request.POST.get('action', 'mark')

        # handle game engine updates
        if action == 'mark':
            try:
                col = int(request.POST['cell_col'])
                row = int(request.POST['cell_row'])

                if game.is_free(col=col, row=row):
                    if not game.mark_player(col=col, row=row):
                        context['error'] = 'Unable to set mark, invalid cordiates(col=%s, row=%s)?' % ( col, row )
                else:
                    # unable to mark, already taken
                    context['error'] = 'Unable to set mark, cell already taken'

            except ValueError:
                # str to int conversion most likely
                context['error'] = 'Unable to convert cell values to integers'
            except Exception as e:
                # broad error
                print >> sys.stderr, "Unable to set mark, internal error: %s" % str(e)
                context['error'] = 'Unable to set mark, internal error'

        elif action == 'clear':
            # create a new game board to clear it
            game = GameEngine()

        else:
            context['error'] = 'Invalid form action'

    context['board'] = game.board
    
    # save game state
    request.session['game'] = game.to_dict()

    return render_to_response('tictactoe/game/normal.html', context,context_instance=RequestContext(request))

def ajax_game(request):
    """ Ajax based game """
    return render_to_response('tictactoe/game/ajax.html', context_instance=RequestContext(request))


