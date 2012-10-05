# Create your views here.
from django.template import Context, loader
# from polls.models import Poll
from django.http import HttpResponse


def index(request):
	request.session['pointless_flag']=False
	t = loader.get_template('tictactoegame/index.html')
	c = Context({
	    'latest_poll_list': "hello",
	})
	return HttpResponse(t.render(c))
	# return HttpResponse("blah")

def play(request):#,game_id):
	t = loader.get_template('tictactoegame/play.html')
	# player=Player.objects.get(session=request.session.sessionid)
	
	game_state=[]
	for i in range(3):
		game_state.append([])
		for j in range(3):
			game_state[i].append(0)
	game_state[1][1]=1 #computer move
	game_state[2][2]=2 #human move
	c = Context({
		'game_state': game_state
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
