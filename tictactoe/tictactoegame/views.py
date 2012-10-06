# Create your views here.
from django.template import Context, RequestContext, loader
# from polls.models import Poll
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from tictactoegame.models import Player, Game
from tictactoegame.tictactoeai import TictactoeAi


def index(request):
	if len(Player.objects.filter(session=request.COOKIES['sessionid']))>0:
		return HttpResponseRedirect("/tictactoegame/play")

	t = loader.get_template('tictactoegame/index.html')
	c = RequestContext(request,{
	    'latest_poll_list': "hello",
	})
	return HttpResponse(t.render(c))

def login(request):
	player_name=request.POST['player_name']
	try:
		p = Player.objects.get(name=player_name)

	except:
		p=Player(name=player_name, session=request.COOKIES['sessionid'])
		p.save()
	else:
		p.session=request.COOKIES['sessionid']
	p.save()

	return HttpResponseRedirect("/tictactoegame/play")

def logout(request):
	request.session.flush()
	return HttpResponseRedirect("/tictactoegame/")


def play(request,move_string=""):
	t = loader.get_template('tictactoegame/play.html')
	message=""
	try:
		p = Player.objects.get(session=request.COOKIES['sessionid'])
	except:
		#player not found? should have logged in, there are no doubt better ways...
		HttpResponseRedirect("/tictactoegame/login")
	else:
		active_game_set=p.game_set.filter(is_active=True)
		active_game=""
		if len(active_game_set)==0:
			message="no active games"
			active_game=Game(board='-'*9, player=p, is_active=True)
			ai=TictactoeAi(active_game.board)
			active_game.board=ai.move()
			active_game.save()
		else:
			active_game=active_game_set[0]#todo handle exception of multiple active games
		if len(move_string)==2:
			move_loc=int(move_string[0])*3+int(move_string[1])
			board=list(active_game.board)
			board[move_loc]='o' #human's move choice
			active_game.board=''.join(board)
			#computer moves here
			ai=TictactoeAi(active_game.board)
			active_game.board=ai.move()
			active_game.save()
			if ai.i_won:
				message="computer wins!"

		game_state=[]
		for i in range(3):
			game_state.append([])
			for j in range(3):
				game_state[i].append(active_game.board[i*3+j])

	c = RequestContext(request,{
		'game_state': game_state,
		'message': message
	})
	return HttpResponse(t.render(c))

def newgame(request):
	try:
		p = Player.objects.get(session=request.COOKIES['sessionid'])
	except:
		#player not found? should have logged in, there are no doubt better ways...
		HttpResponseRedirect("/tictactoegame/login")
	else:
		active_game_set=p.game_set.filter(is_active=True)
		for g in active_game_set:
			g.is_active=False
			g.save()
	return HttpResponseRedirect("/tictactoegame/play")

