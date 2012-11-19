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

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from basic_extras.models import MetaBase

from .core import EMPTY, X, O, NUM_POSITIONS, GRID_RE, Grid


class GridField(models.Field):

    description = _(u'A Tic-tac-toe grid.')

    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        kwargs['default'] = Grid()
        kwargs['max_length'] = NUM_POSITIONS
        kwargs['help_text'] = _(u'Positions 1-%(num)s, indicated as unplayed '
            'by "%(empty)s" and played by "%(x)s" or "%(o)s".') % {
                'num': NUM_POSITIONS, 'empty': EMPTY, 'x': X, 'o': O}
        super(GridField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, Grid):
            return value

        if len(value) != NUM_POSITIONS or not GRID_RE.match(value):
            raise ValidationError('Invalid input for Grid instance.')

        return Grid(value)

    def get_prep_value(self, value):
        return value.__unicode__()

    def get_internal_type(self):
        return 'CharField'


class Game(MetaBase):
    """ A game of Tic-tac-toe played by one person against the program. """

    grid = GridField(_(u'grid'))
    # TODO: Denormalize result data.

    class Meta:
        ordering = ('-created', 'id')
        verbose_name = _(u'game')
        verbose_name_plural = _(u'games')

    def __unicode__(self):
        # TODO: Format the time pretty-like.
        return '%s on %s' % (self.grid.__unicode__(), self.created)

    def game_over(self):
        # NOTE: Again we assume that a filled grid is a complete game. (Though
        # a game can be complete at a draw with only eight moves, this works
        # for now.)
        return self.grid.is_complete()
