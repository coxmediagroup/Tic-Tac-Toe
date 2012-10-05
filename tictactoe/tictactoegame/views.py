# Create your views here.
from django.template import Context, RequestContext, loader
# from polls.models import Poll
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from tictactoegame.models import Player, Game
from tictactoegame.tictactoeai import TictactoeAi


def index(request):
	request.session['pointless_flag']=False
	t = loader.get_template('tictactoegame/index.html')
	c = RequestContext(request,{
	    'latest_poll_list': "hello",
	})
	return HttpResponse(t.render(c))
	# return HttpResponse("blah")

def login(request):
	player_name=request.POST['player_name']
	try:
		p = Player.objects.get(name=player_name)
	except:
		p=Player(name=player_name, session=request.COOKIES['sessionid'])
		p.save()
	else:
		p.session=request.COOKIES['sessionid']
		
		# p.session=request.session.sessionid
		# p.name=player_name

    # try:
    #     selected_choice = p.choice_set.get(pk=request.POST['choice'])
    # except (KeyError, Choice.DoesNotExist):
    #     # Redisplay the poll voting form.
    #     return render_to_response('polls/detail.html', {
    #         'poll': p,
    #         'error_message': "You didn't select a choice.",
    #     }, context_instance=RequestContext(request))
    # else:
    #     selected_choice.votes += 1
    #     selected_choice.save()
    #     # Always return an HttpResponseRedirect after successfully dealing
    #     # with POST data. This prevents data from being posted twice if a
    #     # user hits the Back button.
    #     return HttpResponseRedirect(reverse('polls.views.results', args=(p.id,)))
	# return HttpResponse("junk")
	return HttpResponseRedirect("/tictactoegame/play")

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

		game_state=[]
		for i in range(3):
			game_state.append([])
			for j in range(3):
				game_state[i].append(active_game.board[i*3+j])
		# game_state[1][1]='x' #computer move
		# game_state[2][2]='o' #human move
	c = RequestContext(request,{
		'game_state': game_state,
		'message': message
	})
	return HttpResponse(t.render(c))

def move(request, move_string):
	return HttpResponse("junk")


	# return HttpResponse("You're looking at poll %s." % poll_id)

# def post_comment(request, new_comment):
#     if request.session.get('has_commented', False):
#         return HttpResponse("You've already commented.")
#     c = comments.Comment(comment=new_comment)
#     c.save()
#     request.session['has_commented'] = True
#     return HttpResponse('Thanks for your comment!')
def session_check(request):
	if request.session.get('pointless_flag',True):# and request.session['pointless_flag']==1:
		return HttpResponse("already activated pointless_flag")
	else:
		request.session['pointless_flag']=True
		return HttpResponse("pointless_flag was off, but it's on now!")

#     if request.session.get('has_commented', False):
#         return HttpResponse("You've already commented.")
#     c = comments.Comment(comment=new_comment)
#     c.save()
#     request.session['has_commented'] = True
#     return HttpResponse('Thanks for your comment!')
