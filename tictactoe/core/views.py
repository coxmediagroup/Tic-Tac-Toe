import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from core.forms import SignupForm
from core.game import Game, PLAYER, COMPUTER
from core.models import GameHistory

@login_required
def play_game(request):
    '''
    Loads a new game
    '''
    context = {}
    user = request.user
    context['user'] = user

    # Fetch game counts and records for this player
    game_history = GameHistory.objects.create(player=user)
    all_games = GameHistory.objects.filter(player=user)
    context['played'] = all_games.exclude(status='in_progress').count()
    context['won'] = all_games.filter(status='won').count()
    context['lost'] = all_games.filter(status='lost').count()
    context['tied'] = all_games.filter(status='tied').count()    
    context['game_history_id'] = game_history.id

    # Create a new blank board    
    context['board'] = [0] * 9
    # This will be used by ajax calls to update the game board
    context['json_board_str'] = json.dumps(context['board'])
    return render_to_response('core/play_game.html', context, context_instance=RequestContext(request))

@login_required
def make_move(request):
    """
    Make the human player's move and then calculate and make computer's move
    """
    # Load board and move information
    board = json.loads(request.GET['board'])
    box = int(request.GET['box'].replace("box_",""))
    game_history_id = request.GET['game_history_id']

    # Make player's move and check game result
    game = Game(board)
    game.make_move(box, PLAYER)
    game_over, winning_combination = game.check_game_over()
    computer_played = False

    # If game is still on calculate computer's move and make it
    if not game_over:
        box = game.best_next_move(COMPUTER)
        game.make_move(box, COMPUTER)
        computer_played = True
        game_over, winning_combination = game.check_game_over()

    # If game is over save game history
    if game_over:
        game_history = GameHistory.objects.get(pk=game_history_id)
        game_history.finish_game(game_over)

    result = {}
    result['computer_played'] = computer_played
    result['box'] = str(box)
    result['game_over'] = game_over
    result['board'] = json.dumps(game.get_board())

    # set winning combinations for highlighting
    if winning_combination:
        result['winning_combination_1'] = str(winning_combination[0])
        result['winning_combination_2'] = str(winning_combination[1])
        result['winning_combination_3'] = str(winning_combination[2])

    result['winning_combination'] = winning_combination
    return HttpResponse(json.dumps(result), mimetype='application/json')

@login_required
def logout_user(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return HttpResponseRedirect('/')

def sign_up(request):
    """
    Sign up new user, log them in and redirect to new game
    """
    context = {}
    if request.POST:
        form = SignupForm(request.POST)
        if form.is_valid():
            username, password = form.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect("/")
    else:
        form = SignupForm()
    context['form'] = form    
    return render_to_response('registration/sign_up.html', context, context_instance=RequestContext(request))
