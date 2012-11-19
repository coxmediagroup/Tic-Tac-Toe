"""
Because of the time constraints we are working in, we make a fiew assumptions.

* X always goes first.
* X is the program.
* O is the user.
* Even in a draw all posiitons are marked.

Future improvements:

* Decouple the app and the solver. (See assumptions above.)
* Allow users to view their game history.
"""
import re

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from basic_extras.models import MetaBase


EMPTY_MARK = u'_'
X_MARK = u'x'
O_MARK = u'o'


class Grid(object):
    """
    A grid in a game of Tic-tac-toe.

    Unplayed positions are represented by ``_``. Played positions are
    represented by ``x`` or ``o``.
    """

    # TODO: Learn if there is a more graceful way to handle all these args and
    # there common default value.
    def __init__(self, p1=EMPTY_MARK, p2=EMPTY_MARK, p3=EMPTY_MARK,
            p4=EMPTY_MARK, p5=EMPTY_MARK, p6=EMPTY_MARK, p7=EMPTY_MARK,
            p8=EMPTY_MARK, p9=EMPTY_MARK):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.p5 = p5
        self.p6 = p6
        self.p7 = p7
        self.p8 = p8
        self.p9 = p9

    def __unicode__(self):
        return ''.join([self.p1, self.p2, self.p3, self.p4, self.p5, self.p6,
                       self.p7, self.p8, self.p9])


class GridField(models.Field):

    description = _(u'A Tic-tac-toe grid.')

    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        kwargs['default'] = Grid()
        kwargs['max_length'] = 9
        kwargs['help_text'] = _(u'Positions 1-9, indicated as unplayed by "_" '
                                'and played by "x" or "o".')
        super(GridField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, Grid):
            return value

        # TODO: Do we need the ``{1}`` limiter? Write tests to find out.
        args = re.findall(r'[_xo]{1}', value)
        if len(args) != 9:
            raise ValidationError('Invalid input for Grid instance.')

        return Grid(*args)

    def get_prep_value(self, value):
        # TODO: DRY this -- Grid.__unicode__ uses the same logic.
        return ''.join([value.p1, value.p2, value.p3, value.p4, value.p5,
                       value.p6, value.p7, value.p8, value.p9])

    def get_internal_type(self):
        return 'CharField'

    # def value_to_string(self, obj):
    #     value = self._get_val_from_obj(obj)
    #     return self.get_prep_value(value)


class Game(MetaBase):
    """ A game of Tic-tac-toe played by one person against the program. """

    grid = GridField(_(u'grid'))

    class Meta:
        ordering = ('-modified', 'id')
        verbose_name = _(u'game')
        verbose_name_plural = _(u'games')

    def __unicode__(self):
        # TODO: Format the time pretty.
        return '%s on %s' % (self.grid.__unicode__(), self.created)

    # TODO: Denormalize result data.
    # TODO: Add method to indicate result of game.
    # In progress, draw (cat), x won, o won.

    def game_over(self):
        # TODO: Do we need the ``{1}`` limiter? Write tests to find out.
        marks = re.findall(r'[xo]{1}', self.grid.__unicode__())
        return len(marks) == 9

    def can_play(self, mark):
        """ Return true if the given mark (X or O) is allowed to play. """
        if not self.game_over():
            # Again we assume that X went first.
            # TODO: Do we need the ``{1}`` limiter? Write tests to find out.
            xs = re.findall(r'x{1}', self.grid.__unicode__())
            os = re.findall(r'o{1}', self.grid.__unicode__())
            x_turn = len(xs) == len(os)
            return x_turn if mark == X_MARK else not x_turn
        return False

    def next_turn(self):
        return X_MARK if self.can_play(X_MARK) else O_MARK
