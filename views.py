from django.shortcuts import render_to_response

def index(request):

    return render_to_response('tic_tac_toe/tic_tac_toe.html');
