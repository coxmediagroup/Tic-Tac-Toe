from django.db import models

from datetime import datetime

PLAYER_X    =  1
PLAYER_NONE =  0
PLAYER_O    = -1

class Game(models.Model):
    is_user_x    = models.BooleanField(default=True)
    started      = models.DateTimeField(auto_now_add=True)
    ended        = models.DateTimeField(null=True, default=None)
    
    __board_by_col = (('upper_left'   ,'center_left'  ,'lower_left'  ),
                      ('upper_center' ,'center'       ,'lower_center'),
                      ('upper_right'  ,'center_right' ,'lower_right' ))
    __board_by_row = (('upper_left'   ,'upper_center' ,'upper_right'  ),
                      ('center_left'  ,'center'       ,'center_right'),
                      ('lower_left'   ,'lower_center' ,'lower_right' ))
    __board_by_diag = (('upper_left'  ,'center'       ,'lower_right'),
                       ('upper_right' ,'center'       ,'lower_left'))
    __winning_sets  = tuple(list(__board_by_col) + list(__board_by_row) \
                          + list(__board_by_diag))

    class __col_class(object):
        def __init__(self, game, col_group):
            # self.__class__ is perhaps bad, but 
            # this class won't/shouldn't-be sub-classed
            super(self.__class__, self).__init__()
            self.game = game
            self.col_group = col_group

        def __getitem__(self, cell):
            if cell < 0 or cell > 2:
                raise Exception('Invalid Index %d' % cell)
            return self.game._board.__dict__[self.col_group[cell]]

        def __setitem__(self, cell, val):
            if cell < 0 or cell > 2:
                raise Exception('Invalid Index %d' % cell)
            assert val != PLAYER_NONE and val == self.game.who_moves()
            assert self.game._board.__dict__[self.col_group[cell]] == PLAYER_NONE
            self.game._board.__dict__[self.col_group[cell]] = val
            self.game._board.save()

            state = self.game._determine_state()
            if state[1]:
                self.game.ended = datetime.now()

    @classmethod
    def create_new(cls):
        game = Game()
        game.save()

        board = Board()
        board.game = game
        board.save()

        assert game._board == board

        return game

    def __getitem__(self, col):
        if col < 0 or col > 2:
            raise Exception('Invalid Index %d' % col)
        return Game.__col_class(self, self.__board_by_col[col])

    def _determine_state(self):
       # offsets
       winner   = 0
       complete = 1
       move     = 2
       state = [PLAYER_NONE, True, PLAYER_NONE]

       board_sum = 0
       for group in self.__winning_sets:
           group_sum = 0
           for cell_name in group:
               cell_value = self._board.__dict__[cell_name]
               group_sum += cell_value
               if cell_value == PLAYER_NONE:
                   state[complete] = False
           if group in self.__board_by_col:
               board_sum += group_sum
           if abs(group_sum) == 3:
               state[winner] = group_sum/3
               state[complete] = True
               state[move] = PLAYER_NONE
               return state
       if not state[complete]:
           state[move] = PLAYER_X if board_sum == 0 else PLAYER_O
       return state

    def who_moves(self):
        return self._determine_state()[2]

    def is_complete(self):
        return self._determine_state()[1]

    def who_won(self):
        return self._determine_state()[0]

    def winning_move(self, for_player):
        win_condition_value = for_player*2
        for grp in self.__winning_sets:
            vals = [self._board.__dict__[cell] for cell in grp]
            tot = sum(vals)
            if tot == win_condition_value:
                if grp in self.__board_by_col:
                    return (self.__board_by_col.index(grp), vals.index(0))
                elif grp in self.__board_by_row:
                    return (vals.index(0), self.__board_by_row.index(grp))
                elif grp in self.__board_by_diag:
                    index = vals.index(0)
                    if index == 1:
                        return (1,1)
                    elif grp == self.__board_by_diag[0]:
                        return (index, index)
                    else:
                        return (2,0) if index == 0 else (0,2)
                else:
                    raise Exception('Invalid state in determing winning move')
        return None

class Board(models.Model):
    game         = models.OneToOneField(Game, related_name='_board')
    upper_left   = models.SmallIntegerField(default=0)
    upper_center = models.SmallIntegerField(default=0)
    upper_right  = models.SmallIntegerField(default=0)
    center_left  = models.SmallIntegerField(default=0)
    center       = models.SmallIntegerField(default=0)
    center_right = models.SmallIntegerField(default=0)
    lower_left   = models.SmallIntegerField(default=0)
    lower_center = models.SmallIntegerField(default=0)
    lower_right  = models.SmallIntegerField(default=0)
    last_played  = models.DateTimeField(auto_now=True)

