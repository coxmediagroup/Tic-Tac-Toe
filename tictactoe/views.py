from django.template import Context, loader
from django.http import HttpResponse

def start(request):
    EMPTY = 'not-selected'
    USER = 'user-selected'
    COMPUTER = 'computer-selected'
    
    # prime the board with empty selections
    #board = [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]
    board = [EMPTY, COMPUTER, EMPTY, USER, USER, COMPUTER, USER, COMPUTER, EMPTY]
    
    t = loader.get_template('home.html')
    c = Context({
        'board': board,
    })
    
    return HttpResponse(t.render(c))