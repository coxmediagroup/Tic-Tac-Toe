from django.shortcuts import render_to_response

def index(request):
    return render_to_response('tictactoe.html', {'board': [['x','x','o'],['o','o','x'],['x','x','o']]})
    return HttpResponse("Tic Tac Toe enabled.")
