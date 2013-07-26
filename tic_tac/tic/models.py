import logging
import json


from django.db import models


from tictactoe import getComputerMove, drawBoard


logging.basicConfig(filename='tic_tac.log', level=logging.INFO)
log = logging.getLogger(__name__)

class Person(models.Model):
    name = models.CharField(max_length=128, default='No Name')


class GameSquare(models.Model):
    value = models.CharField(max_length=1, default='n')  # 'x', 'o', 'n' (for null)

    @property
    def has_value(self):
        if self.value =='n':
            return False
        return True

    def __str__(self):
        if self.has_value:
            return self.value
        return 'null'


class GameBoard(models.Model):
    '''
    Row 1: 11, 12, 13
    Row 2: 21, 22, 23
    Row 3: 31, 32, 33
    '''
    square11 = models.ForeignKey(GameSquare, null=True, related_name='gameboard_11')
    square12 = models.ForeignKey(GameSquare, null=True, related_name='gameboard_12')
    square13 = models.ForeignKey(GameSquare, null=True, related_name='gameboard_13')
    square21 = models.ForeignKey(GameSquare, null=True, related_name='gameboard_21')
    square22 = models.ForeignKey(GameSquare, null=True, related_name='gameboard_22')
    square23 = models.ForeignKey(GameSquare, null=True, related_name='gameboard_23')
    square31 = models.ForeignKey(GameSquare, null=True, related_name='gameboard_31')
    square32 = models.ForeignKey(GameSquare, null=True, related_name='gameboard_32')
    square33 = models.ForeignKey(GameSquare, null=True, related_name='gameboard_33')

    def __str__(self):
        r = {}
        r['id'] = self.id
        r['11'] = str(self.square11)
        r['12'] = str(self.square12)
        r['13'] = str(self.square13)
        r['21'] = str(self.square21)
        r['22'] = str(self.square22)
        r['23'] = str(self.square23)
        r['31'] = str(self.square31)
        r['32'] = str(self.square32)
        r['33'] = str(self.square33)
        return json.dumps(r)

    def __unicode__(self):
        return str(self)

    def update(self, nb):
        for k, v in nb.iteritems():
            if k == '11' and v in [u'x', u'o']:
                self.square11.value = v
            if k == '12' and v in [u'x', u'o']:
                self.square12.value = v
            if k == '13' and v in [u'x', u'o']:
                self.square13.value = v
            if k == '21' and v in [u'x', u'o']:
                self.square21.value = v
            if k == '22' and v in [u'x', u'o']:
                self.square22.value = v
            if k == '23' and v in [u'x', u'o']:
                self.square23.value = v
            if k == '31' and v in [u'x', u'o']:
                self.square31.value = v
            if k == '32' and v in [u'x', u'o']:
                self.square32.value = v
            if k == '33' and v in [u'x', u'o']:
                self.square33.value = v

    def game_won(self, v):
        if self.square11.value == v and \
           self.square12.value == v and \
           self.square13.value == v: return True
        if self.square21.value == v and \
           self.square22.value == v and \
           self.square23.value == v: return True
        if self.square31.value == v and \
           self.square32.value == v and \
           self.square33.value == v: return True
        if self.square11.value == v and \
           self.square21.value == v and \
           self.square31.value == v: return True
        if self.square12.value == v and \
           self.square22.value == v and \
           self.square32.value == v: return True
        if self.square13.value == v and \
           self.square23.value == v and \
           self.square33.value == v: return True
        if self.square11.value == v and \
           self.square22.value == v and \
           self.square33.value == v: return True
        if self.square13.value == v and \
           self.square22.value == v and \
           self.square31.value == v: return True
        return False

    def translate(self):
        translated_board = " {}{}{}{}{}{}{}{}{}".format(
            self.square11.value, self.square12.value, self.square13.value,
            self.square21.value, self.square22.value, self.square23.value,
            self.square31.value, self.square32.value, self.square33.value)
        translated_board = translated_board.replace('n',' ')
        translated_board = translated_board.upper()
        return translated_board
 
    def AI_move(self):
        """Translate the current board to a form that our 3rd party API
        can understand, pass it to the Tic-Tac-Toe AI, and make a move.

        Right now, allow the Player to be Xs always."""
        translated_board = self.translate()
        move = getComputerMove(translated_board, 'O')
        if move == 1:
            self.square11.value = 'o'
        if move == 2:
            self.square12.value = 'o'
        if move == 3:
            self.square13.value = 'o'
        if move == 4:
            self.square21.value = 'o'
        if move == 5:
            self.square22.value = 'o'
        if move == 6:
            self.square23.value = 'o'
        if move == 7:
            self.square31.value = 'o'
        if move == 8:
            self.square32.value = 'o'
        if move == 9:
            self.square33.value = 'o'

    def simple_display(self):
        t_board = self.translate()
        return drawBoard(t_board)


class Game(models.Model):
    player = models.ForeignKey(Person)


