import json

from django.core.cache import cache
from django.http import HttpResponse
from django.template import RequestContext, loader

# Just one static view
def index(request):
    template = loader.get_template('tic_tac_toe/index.html')
    context = RequestContext(request, {
    })
    cache.set('squares', None, 10)
    return HttpResponse(template.render(context))

# helper function for AI, so my head does not hurt
def __check_for_win_or_block(squares, index, can_block_index, ai, side, x2, x3):
    if (index == -1 and squares[x2] == side):
        if (squares[x3] == ""):
            if (side == ai):
                index = x3 # win!
            else:
                can_block_index = x3
    if (index == -1 and squares[x3] == side):
        if (squares[x2] == ""):
            if (side == ai):
                index = x2 # win!
            else:
                can_block_index = x2
    return index, can_block_index

# Process AI turn (to prevent player from being able to cheat)
def ai(request):
    data = None
    valid = True
    differences = 0
    squares = json.loads(request.POST["squares"])
    ai = request.POST["ai"]
    player = "X"
    if (ai == "X"):
        player = "O"

    if (cache.get('squares') == None):
        cache.set('squares', squares, 600)
        differences = 1
    else:
        old_squares = cache.get('squares')
        nothing = None
        for index in range(9):
            if (old_squares[index] == "") and (squares[index] != old_squares[index]):
                differences = differences + 1
            elif (old_squares[index] != squares[index]):
                valid = False
                break
        if valid and (differences > 1):
            valid = False

    if not valid:
        data = {"success": False, "error": -1}
    elif (differences == 0):
        data = {"success": True, "move_index": -1}
    else:
        index = -1
        # 0, 1, 2  ||  X, X, X
        # 3, 4, 5  ||  X, 4, 5
        # 6, 7, 8  ||  6, 7, 8

        # check if AI can win/block player
        #  on this side, each one needs to be check twice from two different points
        #  to prevent the AI from letting the player win 
        #  EXAMPLE: if check 0 -> 1 -> 2 and 0 is empty, but 1 and 2 are not, 
        #   it will return false unless 1 -> 0 -> 2 or 2 -> 1 -> 0 is checked
        can_block_index = -1
        # check 0
        if (squares[0] != ""):
            side = squares[0]
            # 0, 1, 2
            index, can_block_index = __check_for_win_or_block(squares, index, can_block_index, ai, side, 1, 2)
            # 0, 3, 6
            index, can_block_index = __check_for_win_or_block(squares, index, can_block_index, ai, side, 3, 6)
            # 0, 4, 8
            index, can_block_index = __check_for_win_or_block(squares, index, can_block_index, ai, side, 4, 8)
        # check 1
        if (index == -1 and squares[1] != ""):
            side = squares[1]
            # 1, 4, 7
            index, can_block_index = __check_for_win_or_block(squares, index, can_block_index, ai, side, 4, 7)
        # check 2
        if (index == -1 and squares[2] != ""):
            side = squares[2]
            # 0, 1, 2
            index, can_block_index = __check_for_win_or_block(squares, index, can_block_index, ai, side, 0, 1)
            # 2, 4, 6
            index, can_block_index = __check_for_win_or_block(squares, index, can_block_index, ai, side, 4, 6)
            # 2, 5, 8
            index, can_block_index = __check_for_win_or_block(squares, index, can_block_index, ai, side, 5, 8)
        # check 3
        if (index == -1 and squares[3] != ""):
            side = squares[3]
            # 3, 4, 5
            index, can_block_index = __check_for_win_or_block(squares, index, can_block_index, ai, side, 4, 5)
            # 0, 3, 6
            index, can_block_index = __check_for_win_or_block(squares, index, can_block_index, ai, side, 0, 6)
        # check 4
        if (index == -1 and squares[4] != ""):
            side = squares[4]
            # 0, 4, 8
            index, can_block_index = __check_for_win_or_block(squares, index, can_block_index, ai, side, 0, 8)
            # 1, 4, 7
            index, can_block_index = __check_for_win_or_block(squares, index, can_block_index, ai, side, 1, 7)
            # 2, 4, 6
            index, can_block_index = __check_for_win_or_block(squares, index, can_block_index, ai, side, 2, 6)
        # check 5
        if (index == -1 and squares[5] != ""):
            side = squares[5]
            # 2, 5, 8
            index, can_block_index = __check_for_win_or_block(squares, index, can_block_index, ai, side, 2, 8)
            # 3, 4, 5
            index, can_block_index = __check_for_win_or_block(squares, index, can_block_index, ai, side, 3, 4)
        # check 6
        if (index == -1 and squares[6] != ""):
            side = squares[6]
            # 6, 7, 8
            index, can_block_index = __check_for_win_or_block(squares, index, can_block_index, ai, side, 7, 8)
        # check 7
        if (index == -1 and squares[7] != ""):
            side = squares[7]
            # 6, 7, 8
            index, can_block_index = __check_for_win_or_block(squares, index, can_block_index, ai, side, 6, 8)

        if (index == -1):
            # block player
            if (can_block_index != -1):
                index = can_block_index
            else:
                # prevent player for getting two oppsite corners
                #  or get two opposite corners
                if (squares[0] != ""):
                     if (squares[8] == ""): 
                         index = 8
                if (index == -1 and squares[8] != ""):
                     if (squares[0] == ""): 
                         index = 0
                if (index == -1 and squares[2] != ""):
                     if (squares[6] == ""): 
                         index = 6
                if (index == -1 and squares[6] != ""):
                     if (squares[2] == ""): 
                         index = 2           
                if (index == -1):
                    # go for some corner
                    for test_index in [0, 2, 6, 8]:
                        if (squares[test_index] == ""):
                            index = test_index
                    # go for center    
                    if (index == -1 and squares[4] == ""):
                        index = 4
                    elif (index == -1):
                        # go for first open space
                        for test_index in [1, 3, 5, 7]:
                            if (squares[test_index] == ""):
                                index = test_index
        if (index == -1):
            data = {"success": False, "error": "Could not find move for AI"}
        else:
            squares[index] = ai
            cache.set('squares', squares, 600)
            data = {"success": True, "move_index": index}

    return HttpResponse(json.dumps(data), content_type="application/json", status=200)

def new(request):
    cache.set('squares', None, 10)
    data = {"success": True}
    return HttpResponse(json.dumps(data), content_type="application/json", status=200)
