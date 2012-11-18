"""
Because of the time constraints we are working in, we make a fiew assumptions.

* X always goes first.
* X is the program.
* O is the user.
* Even in a draw all posiitons are marked.
"""
import re

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from basic_extras.models import MetaBase


GRID_POSITIONS = [1, 2, 3, 4, 5, 6, 7, 8, 9]
GRID_POSITIONS = [(n, n) for n in GRID_POSITIONS]
UNPLAYED_MARK = u'_'
X_PLAYED_MARK = u'x'
O_PLAYED_MARK = u'o'
POSITION_MARKS = (
    (UNPLAYED_MARK, _(u'unplayed')),
    (X_PLAYED_MARK, _(u'x')),
    (O_PLAYED_MARK, _(u'o')),
)


class Grid(object):
    """
    A grid in a game of Tic-tac-toe.

    Unplayed positions are represented by ``_``. Played positions are
    represented by ``x`` or ``o``.
    """

    # TODO: Learn if there is a more graceful way to handle all these args and
    # there common default value.
    def __init__(self, p1='_', p2='_', p3='_', p4='_', p5='_', p6='_', p7='_',
                 p8='_', p9='_'):
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

    def can_play(self, mark):
        # Again we assume that X went first.
        # TODO: Do we need the ``{1}`` limiter? Write tests to find out.
        xs = re.findall(r'x{1}', self.__unicode__())
        os = re.findall(r'o{1}', self.__unicode__())
        x_turn = len(xs) == len(os)
        return x_turn if mark == X_PLAYED_MARK else not x_turn

    def next_turn(self):
        return X_PLAYED_MARK if self.can_play(X_PLAYED_MARK) else O_PLAYED_MARK


class GridField(models.Field):

    description = _(u'A Tic-tac-toe grid.')

    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 9
        kwargs['default'] = Grid()
        kwargs['help_text'] = _(u'Positions 1-9, indicated as unplayed by "_" '
                                'and played by "x" or "o".')
        super(GridField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, Grid):
            return value

        state = re.compile(r'[_xo]{1}')
        args = state.findall(value)
        if len(args) != 9:
            raise ValidationError('Invalid input for Grid instance.')

        return Grid(*args)

    def get_prep_value(self, value):
        return ''.join([value.p1, value.p2, value.p3, value.p4, value.p5,
                       value.p6, value.p7, value.p8, value.p9])

    def get_internal_type(self):
        return 'CharField'

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)


class Game(MetaBase):
    """ A game of Tic-tac-toe played by one person against the program. """

    player = models.ForeignKey(User, verbose_name=_(u'player'), related_name='games')
    grid = GridField(_(u'grid'))
    # TODO: Denormalize turn data.
    # TODO: Denormalize result data.

    class Meta:
        ordering = ('-modified', 'id')
        verbose_name = _(u'game')
        verbose_name_plural = _(u'games')

    def __unicode__(self):
        # TODO: Format the time pretty.
        return '%s on %s' % (self.player.username, self.created)

    # TODO: Add method to indicate whose turn it is. (X always goes first.)
    # TODO: Add method to indicate result of game.
    # In progress, draw (cat), x won, o won.


class Play(MetaBase):
    """ A play in a game of Tic-tac-toe. """

    game = models.ForeignKey(Game, verbose_name=_(u'game'), related_name='plays')
    position = models.PositiveSmallIntegerField(_(u'position'),
        choices=GRID_POSITIONS, help_text=_(u'A number 1-9.'))
    mark = models.CharField(_(u'mark'), max_length=1, choices=POSITION_MARKS,
        default=UNPLAYED_MARK)

    class Meta:
        order_with_respect_to = 'game'
        ordering = ('game', '-created', 'id')
        unique_together = (('position', 'game'),)
        verbose_name = _(u'play')
        verbose_name_plural = _(u'plays')

    def __unicode__(self):
        # TODO: Return game, position, player, and order.
        return self.game.__unicode__()

    def save(self, *args, **kwargs):
        if self.game.grid.can_play(self.mark):
            # self.game.grid.
        else:
            raise ValidationError('Incorrect mark, cannot play out of turn.')

        super(Play, self).save(*args, **kwargs)

    # FIXME: Update the game grid on save.
    # FIXME: Validate that this is a valid play:
    # 1. Marks alternate.
    # 2. Does not overwrite other mark. (Handled by Meta.unique_together.)
