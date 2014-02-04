from django.core.cache import cache

STATE_PLAYER_X_TURN = 'X'
STATE_PLAYER_O_TURN = 'O'
STATE_GAME_OVER = 'OVER'

PLAYER1_WON = 0
PLAYER2_WON = 1
DRAW = 2

BOX_CLEAR = ''
BOX_X = 'X'
BOX_O = 'O'

PLAYER_X = 'X'
PLAYER_O = 'O'

def get_box_state(box):
        return cache.get('tictactoe_box' + str(box))

def try_set_box_state(box, value):
       if cache.get('tictactoe_box' + str(box)) != '':
           return False
       cache.set('tictactoe_box' + str(box), value)
       return True

def opposing_player(player):
    if player == PLAYER_X:
        return PLAYER_O
    else:
        return PLAYER_X

def is_corner(box):
    if box == 1 or box == 3 or box == 7 or box == 9:
        return True
    return False

def get_opposing_box(box):
    if box == 1:
        return 9
    if box == 3:
        return 7
    if box == 7:
        return 3
    if box == 9:
        return 1
    return None

def get_next_winnable_move(side):
    if get_box_state(1) == side and get_box_state(2) == side and get_box_state(3) != opposing_player(side):
        return 3
    if get_box_state(1) == side and get_box_state(3) == side and get_box_state(2) != opposing_player(side):
        return 2
    if get_box_state(2) == side and get_box_state(3) == side and get_box_state(1) != opposing_player(side):
        return 1
    if get_box_state(1) == side and get_box_state(9) == side and get_box_state(5) != opposing_player(side):
        return 5
    if get_box_state(1) == side and get_box_state(5) == side and get_box_state(9) != opposing_player(side):
        return 9
    if get_box_state(1) == side and get_box_state(7) == side and get_box_state(4) != opposing_player(side):
        return 4
    if get_box_state(1) == side and get_box_state(4) == side and get_box_state(7) != opposing_player(side):
        return 7
    if get_box_state(7) == side and get_box_state(4) == side and get_box_state(1) != opposing_player(side):
        return 1
    if get_box_state(3) == side and get_box_state(6) == side and get_box_state(9) != opposing_player(side):
        return 9
    if get_box_state(3) == side and get_box_state(9) == side and get_box_state(6) != opposing_player(side):
        return 6
    if get_box_state(6) == side and get_box_state(9) == side and get_box_state(3) != opposing_player(side):
        return 3
    if get_box_state(7) == side and get_box_state(9) == side and get_box_state(8) != opposing_player(side):
        return 8
    if get_box_state(7) == side and get_box_state(8) == side and get_box_state(9) != opposing_player(side):
        return 9
    if get_box_state(8) == side and get_box_state(9) == side and get_box_state(7) != opposing_player(side):
        return 7
    if get_box_state(2) == side and get_box_state(5) == side and get_box_state(8) != opposing_player(side):
        return 8
    if get_box_state(2) == side and get_box_state(8) == side and get_box_state(5) != opposing_player(side):
        return 5
    if get_box_state(5) == side and get_box_state(8) == side and get_box_state(2) != opposing_player(side):
        return 2
    if get_box_state(4) == side and get_box_state(5) == side and get_box_state(6) != opposing_player(side):
        return 6
    if get_box_state(4) == side and get_box_state(6) == side and get_box_state(5) != opposing_player(side):
        return 5
    if get_box_state(5) == side and get_box_state(6) == side and get_box_state(4) != opposing_player(side):
        return 4

    return None



class GameBoard:
    def __init__(self, computer_side):
        self.side = computer_side
        self.reset()

    def reset(self):
        self.turn_count = 0
        self.last_move = 0
        self.human_last_move = 0
        self.state = STATE_PLAYER_X_TURN

        cache.set('tictactoe_box1', '')
        cache.set('tictactoe_box2', '')
        cache.set('tictactoe_box3', '')
        cache.set('tictactoe_box4', '')
        cache.set('tictactoe_box5', '')
        cache.set('tictactoe_box6', '')
        cache.set('tictactoe_box7', '')
        cache.set('tictactoe_box8', '')
        cache.set('tictactoe_box9', '')


    def computer_move(self):

        self.turn_count += 1

        if self.state == opposing_player(self.side):
            return None

        #handle each turn based on count
        if self.turn_count == 1:
            #always go top-left on first turn
            try_set_box_state(1, self.side)
            ret = 1

        elif self.turn_count == 2:
            #see if they went in a corner, if so, counter it
            if is_corner(self.human_last_move):
                ret = get_opposing_box(self.human_last_move)
                try_set_box_state(ret, self.side)
            #since no corner was taken, take top-left
            else:
                try_set_box_state(1, self.side)
                ret = 1
        elif self.turn_count == 3:
            #if our last move was in a corner
            if is_corner(self.last_move):
                opposing_box = get_opposing_box(self.last_move)
                #try to get the opposing corner
                val = try_set_box_state(opposing_box)
                if val is True:
                    ret = opposing_box
                #human player went there, so lets go to adjacent corner
                else:
                    ret = 3
                    try_set_box_state(ret, self.side)
        elif self.turn_count == 4:
            #if human player has winning move, counter that
            winning_box = get_next_winnable_move(opposing_player(self.side))
            if winning_box is not None:
                ret = winning_box
                try_set_box_state(winning_box, self.side)
            #there is no winning move, so let's set one up for ourselves
            else:
                if try_set_box_state(3,self.side):
                    ret = 3
                elif try_set_box_state(7, self.side):
                    ret = 7

       # elif self.turn_count == 5:
       # elif self.turn_count == 6:
       # elif self.turn_count == 7:
       # elif self.turn_count == 8:
       # else:

        self.state = opposing_player(self.side)
        self.last_move = ret

        return ret

