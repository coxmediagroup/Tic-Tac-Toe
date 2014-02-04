from django.core.cache import cache

STATE_PLAYER_X_TURN = 0
STATE_PLAYER_O_TURN = 1
STATE_GAME_OVER = 2

PLAYER1_WON = 0
PLAYER2_WON = 1
DRAW = 2

BOX_CLEAR = ''
BOX_X = 'X'
BOX_O = 'O'

PLAYER_X = 'X'
PLAYER_O = 'O'

class GameBoard:
    def __init__(self, computer_side):
        side = computer_side
        self.reset()

    def reset(self):
        turn_count = 1
        state = STATE_PLAYER_X_TURN
        cache.set('tictactoe_box1', '')
        cache.set('tictactoe_box2', '')
        cache.set('tictactoe_box3', '')
        cache.set('tictactoe_box4', '')
        cache.set('tictactoe_box5', '')
        cache.set('tictactoe_box6', '')
        cache.set('tictactoe_box7', '')
        cache.set('tictactoe_box8', '')
        cache.set('tictactoe_box9', '')

    def get_box_state(self, box):
        return cache.get('tictactoe_box' + box)

    def try_set_box_state(self, box, value):
       if cache.get('tictactoe_box' + box) != '':
           return False

       cache.set('tictactoe_box' + box, value)
       return True

    def computer_move(self):
        self.turn_count += 1

        if self.state == STATE_PLAYER_X_TURN and self.side == PLAYER_O:
            return
        if self.state == STATE_PLAYER_O_TURN and self.side == PLAYER_X:
            return

        #handle each turn based on count
        if self.turn_count == 1:
            #always go top left on first turn
            self.try_set_box_state(1, self.side)
        elif self.turn_count == 2:
            #see if they went in a corner, if so, counter it
            if self.get_box_state(1) == self.side:
            elif self.get_box_state(1) == self.side:
            elif self.get_box_state(1) == self.side:
            elif self.get_box_state(1) == self.side:
            else:


        elif self.turn_count == 3:
        elif self.turn_count == 4:
        elif self.turn_count == 5:
        elif self.turn_count == 6:
        elif self.turn_count == 7:
        elif self.turn_count == 8:
        else:

