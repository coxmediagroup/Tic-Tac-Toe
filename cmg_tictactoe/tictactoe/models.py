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

from .core import Grid


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
        ordering = ('-created', 'id')
        verbose_name = _(u'game')
        verbose_name_plural = _(u'games')

    def __unicode__(self):
        # TODO: Format the time pretty.
        return '%s on %s' % (self.grid.__unicode__(), self.created)

    # TODO: Denormalize result data.
    # TODO: Add method to indicate result of game.In progress, draw (cat),
    # X won, O won.

    def game_over(self):
        # NOTE: Again we assume that a filled grid is a complete game. (Though
        # a game can be complete at a draw with only eight moves, this works
        # for now.)
        return self.grid.is_filled()
