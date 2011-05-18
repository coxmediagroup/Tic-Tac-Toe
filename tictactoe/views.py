from django.template import Context, loader
from django.http import HttpResponse
from django.core.cache import cache
from random import choice

def is_winner(p, b):
    # p is for player (USER or COMPUTER);
    # b is for the board
    
    return ((b[0] == p and b[1] == p and b[2] == p) or # across the top
        (b[3] == p and b[4] == p and b[5] == p) or # across the middle
        (b[6] == p and b[7] == p and b[8] == p) or # across the bottom
        (b[0] == p and b[3] == p and b[6] == p) or # down the left side
        (b[1] == p and b[4] == p and b[7] == p) or # down the middle
        (b[2] == p and b[5] == p and b[8] == p) or # down the right
        (b[0] == p and b[4] == p and b[8] == p) or # left diagonal
        (b[2] == p and b[4] == p and b[6] == p)) # right diagonal

def is_board_full(board, EMPTY):
    for i in range(9):
        if board[i] == EMPTY:
            return false
    
    return true
        
def get_computer_move(board, USER, COMPUTER, EMPTY):
    # see if a winning move is possible
    for i in range(9):
        board_copy = board[:]
        if board_copy[i] == EMPTY:
            board_copy[i] = COMPUTER
        if is_winner(COMPUTER, board_copy):
            return i

    # check if player could win on the next move and block them
    for i in range(9):
        board_copy = board[:]
        if board_copy[i] == EMPTY:
            board_copy[i] = USER
            if is_winner(USER, board_copy):
                return i
                
    # take a random corner, if it's free
    corners = [0, 2, 6, 8]
    while corners:
        random_corner = choice(corners)
        if board[random_corner] == EMPTY:
            return random_corner
        else:
            corners = [value for value in corners[:] if value != random_corner]
            
    # take the center, if it's free
    if board[4] == EMPTY:
        return 4
        
    # randomly choose one of the remaining side space    
    sides = [1, 3, 5, 7]
    while sides:
        random_side = choice(sides)
        if board[random_side] == EMPTY:
            return random_side
        else:
            sides = [value for value in sides[:] if value != random_side]
    
def start(request):
    EMPTY = 'not-selected'
    USER = 'user-selected'
    COMPUTER = 'computer-selected'
    
    EMPTY_BOARD = [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]
    
    selected_cell = request.GET.get('selected_cell', None)
        
    if request.method == 'GET' and selected_cell:
        # ensure the value is not already set (i.e. refresh button was pressed
        # with the GET value in the URL)        
        current_board = cache.get('board')
        if current_board and not current_board[int(selected_cell)] in (USER, COMPUTER):
            #update the current board with the user's move and a follow-up move from the computer
            current_board[int(selected_cell)] = USER
            current_board[get_computer_move(current_board, USER, COMPUTER, EMPTY)] = COMPUTER
            board = current_board
            cache.set('board', board)
        else: # move already made - return the same board
            board = current_board
    else:
        # prime the board with empty selections
        board = EMPTY_BOARD 
        
        # store the board in cache
        cache.set('board', board)
    
    t = loader.get_template('home.html')
    c = Context({
        'board': board,
    })
    
    return HttpResponse(t.render(c))