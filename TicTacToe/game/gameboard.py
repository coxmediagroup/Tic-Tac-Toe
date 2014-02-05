from django.core.cache import cache

STATE_PLAYER_X_TURN = 'X'
STATE_PLAYER_O_TURN = 'O'
STATE_GAME_OVER = 'OVER'

HUMAN_WON = 0
COMPUTER_WON = 1
DRAW = 2

BOX_CLEAR = ''
BOX_X = 'X'
BOX_O = 'O'

PLAYER_X = 'X'
PLAYER_O = 'O'



def get_side_won(side):
    #check column 1
    if get_box_state(1) == side and get_box_state(4) == side and get_box_state(7) == side:
        return True
    #...col2
    if get_box_state(2) == side and get_box_state(5) == side and get_box_state(8) == side:
        return True
    if get_box_state(3) == side and get_box_state(6) == side and get_box_state(9) == side:
        return True

    #check rows
    #for i in range(1,7,3):
    if get_box_state(1) == side and get_box_state(2) == side and get_box_state(3) == side:
        return True
    if get_box_state(4) == side and get_box_state(5) == side and get_box_state(6) == side:
        return True
    if get_box_state(7) == side and get_box_state(8) == side and get_box_state(9) == side:
        return True

    #diagonals
    if get_box_state(1) == side and get_box_state(5) == side and get_box_state(9) == side:
        return True
    if get_box_state(3) == side and get_box_state(5) == side and get_box_state(7) == side:
        return True

    return False


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

def box_empty(box):
    return get_box_state(box) == BOX_CLEAR


def get_opposing_corner(box):
    if box == 1:
        return 9
    if box == 3:
        return 7
    if box == 7:
        return 3
    if box == 9:
        return 1
    return None

def get_adjacent_corners(box):
    if get_box_state(box) == 1:
        return 3, 7
    if get_box_state(box) == 3:
        return 1, 9
    if get_box_state(box) == 7:
        return 1, 9
    if get_box_state(box) == 9:
        return 3, 7



def get_empty_adjacent_box(box):
    if box == 1:
        if get_box_state(3) == '':
            return 3
        elif get_box_state(7) == '':
            return 7
        else:
            return None

    if box == 3:
        if get_box_state(1) == '':
            return 1
        elif get_box_state(9) == '':
            return 9
        else:
            return None

    if box == 7:
        if get_box_state(1) == '':
            return 1
        elif get_box_state(9) == '':
            return 9
        else:
            return None

    if box == 9:
        if get_box_state(3) == '':
            return 3
        elif get_box_state(7) == '':
            return 7
        else:
            return None

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
    #diagonals
    if get_box_state(1) == side and get_box_state(5) == side and get_box_state(9) != opposing_player(side):
        return 9
    if get_box_state(1) == side and get_box_state(9) == side and get_box_state(5) != opposing_player(side):
        return 5
    if get_box_state(5) == side and get_box_state(9) == side and get_box_state(1) != opposing_player(side):
        return 1
    if get_box_state(7) == side and get_box_state(5) == side and get_box_state(3) != opposing_player(side):
        return 3
    if get_box_state(7) == side and get_box_state(3) == side and get_box_state(5) != opposing_player(side):
        return 5
    if get_box_state(3) == side and get_box_state(5) == side and get_box_state(7) != opposing_player(side):
        return 7


    return None



def get_forking_box(side):
    #get a corner
    for corner in [1, 3, 7, 9]:
        if get_box_state(corner) == side:
            one, two = get_adjacent_corners(1)
            if get_box_state(one) == side and get_box_state(two) == BOX_CLEAR:
                return two
            if get_box_state(two) == side and get_box_state(one) == BOX_CLEAR:
                return one

    return None

def get_available_box():
    for i in range(1,9):
        if get_box_state(i) == BOX_CLEAR:
            return i
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
        self.winner = DRAW

        cache.set('tictactoe_box1', '')
        cache.set('tictactoe_box2', '')
        cache.set('tictactoe_box3', '')
        cache.set('tictactoe_box4', '')
        cache.set('tictactoe_box5', '')
        cache.set('tictactoe_box6', '')
        cache.set('tictactoe_box7', '')
        cache.set('tictactoe_box8', '')
        cache.set('tictactoe_box9', '')

    @staticmethod
    def get():
        return cache.get('ttt_game_board')

    def save(self):
        cache.set('ttt_game_board', self)

    def check_game_over(self):
        ret = False
        human = opposing_player(self.side)

        if get_available_box() is None:
            self.state = STATE_GAME_OVER
            if get_side_won(self.side):
                self.winner = self.side
            elif get_side_won():
                self.winner = human
            else:
                self.winner = DRAW
            ret = True

        #save it
        self.save()


    def get_game_variables(self):
        ret = {}
        ret['box1'] = get_box_state(1)
        ret['box2'] = get_box_state(2)
        ret['box3'] = get_box_state(3)
        ret['box4'] = get_box_state(4)
        ret['box5'] = get_box_state(5)
        ret['box6'] = get_box_state(6)
        ret['box7'] = get_box_state(7)
        ret['box8'] = get_box_state(8)
        ret['box9'] = get_box_state(9)
        ret['game_state'] = self.state
        ret['winner'] = self.winner
        ret['message'] = self.get_player_message()
        return ret

    def set_turn(self, player):
        self.state = player
        self.save()

    def get_player_message(self):
        if opposing_player(self.side) == self.state:
            return 'Your turn!'
        else:
            return "Computer's turn..."

    def human_move(self, box_choice):
        self.turn_count += 1

        human = opposing_player(self.side)
        box_choice = int(box_choice)
        self.human_last_move = box_choice
        try_set_box_state(box_choice, human)

        if get_side_won(human):
            self.state = STATE_GAME_OVER
            self.winner = human

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
                #ret = get_empty_adjacent_box(self.human_last_move)
                #try_set_box_state(ret, self.side)
                #ret = get_opposing_corner(self.human_last_move)

                #take middle
                ret = 5
                try_set_box_state(ret, self.side)
            #since no corner was taken, take top-left
            else:
                try_set_box_state(1, self.side)
                ret = 1
        elif self.turn_count == 3:
            #if our last move was in a corner
            if is_corner(self.last_move):
                opposing_box = get_opposing_corner(self.last_move)
                #try to get the opposing corner
                val = try_set_box_state(opposing_box, self.side)
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
            #there is no winning move, so let's take a side to force player to counter
            else:
                if try_set_box_state(2, self.side):
                    ret = 2
                elif try_set_box_state(4, self.side):
                    ret = 4
                else:
                    try_set_box_state(6, self.side)
                    ret = 6

        #elif self.turn_count == 5:
        #
        #    #see if we can win next move
        #    winning_box = get_next_winnable_move(self.side)
        #    if winning_box is not None:
        #        ret = winning_box
        #        try_set_box_state(winning_box, self.side)
        #        self.state = STATE_GAME_OVER
        #        self.winner = COMPUTER_WON
        #        return ret
        #    #look if we have diagonal
        #    if get_box_state(1) == self.side and get_box_state(9) == self.side:
        #        #since we do have 1 and 9 and couldn't win, human has box 2; go for box 3
        #        val = try_set_box_state(3, self.side)
        #        ret = 3
        #        if val is False: #human took middle, so...
        #            try_set_box_state(7, self.side)
        #            ret = 7
        #     #go for another corner
        #    else:
        #        try_set_box_state(7, self.side)
        #        ret = 7
        elif self.turn_count >= 5:
            #see if we can win next move
            winning_box = get_next_winnable_move(self.side)
            if winning_box is not None:
                ret = winning_box
                try_set_box_state(winning_box, self.side)
                self.state = STATE_GAME_OVER
                self.winner = COMPUTER_WON
                return ret
            else:
                #block a winnable by opponent
                winning_box = get_next_winnable_move(opposing_player(self.side))
                if winning_box is not None:
                    try_set_box_state(winning_box, self.side)
                    ret = winning_box
                else:
                    #try and get the fork
                    val = get_forking_box(self.side)
                    if val is not None:
                        ret = val
                        try_set_box_state(ret, self.side)
                    else:
                        ret = get_available_box()
                        try_set_box_state(ret, self.side)

        self.state = opposing_player(self.side)
        self.last_move = ret

        return ret

