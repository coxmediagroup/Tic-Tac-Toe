import json
from django.shortcuts import render, HttpResponse
from tictactoe.forms import UsernameForm
from tictactoe.models import Player
from lib import minimax



def index(request):
    ctx = {}
    un = request.session.get('username',None)
    if un:
        player_qs = Player.objects.filter(
            username=un
            )
        if player_qs.count() > 0:
            player = player_qs[0]
            rank = Player.objects.all(
                ).filter(
                plays__gte=player.plays
                ).exclude(
                username=player.username
                ).order_by(
                '-plays'
                ).count() + 1
            ctx.update({'player':player,
                'player_rank':rank})

    players = Player.objects.all().order_by('-plays')[:10]
    ctx.update({'players':players})

    return render(request, 'index.html', ctx)

def play_game(request):
    ctx = {}
    if request.method == 'GET':
        username_form = UsernameForm()
        ctx.update({'form':username_form})
    if request.method == 'POST':
        username_form = UsernameForm(request.POST)
        if username_form.is_valid():
            un = username_form.cleaned_data['username']
            request.session['username'] = un
            player, created = Player.objects.get_or_create(username=un)
        else:
            ctx.update({'form':username_form})

    request.session['game_state'] = '---------'
    return render(request, 'game.html', ctx)

def make_move(request):
    if request.method == 'POST':
        ctx = {}

        try:
            player_move = int(request.POST['move'])
        except ValueError:
            ctx.update({'computer_move':'-2'})
            return HttpResponse(json.dumps(ctx),mimetype='application/json')
        game_state = request.session.get('game_state','---------')
        game_state = list(str(game_state))
        game_state[player_move] = 'X'

        score, computer_move = minimax.next_move(game_state,'O')
        if (computer_move == -1) or (score == -1):
            username = request.session.get('username')
            player = Player.objects.get(username=username)
            ctx.update({'cmove':computer_move})
            if computer_move == -1:
                ctx.update({'game_status':'draw'})
            else:
                ctx.update({'game_status':'lose'})
            request.session['game_state'] = '---------'
            player.plays += 1
            player.save()
        else:
            ctx.update({'cmove':str(computer_move)})
            ctx.update({'game_status':'playing'})
            game_state[computer_move] = 'O'
            request.session['game_state'] = ''.join(game_state)

        return HttpResponse(json.dumps(ctx),mimetype='application/json')


    else:
        return HttpResponse(json.dumps({'error':'The URL you requested was improperly accessed.'}),
            mimetype='application/json')
