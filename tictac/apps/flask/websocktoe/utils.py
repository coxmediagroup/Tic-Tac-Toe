# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
import traceback

from apps.coxtactoe import tictactoe as ttt
from apps.coxtactoe.exceptions import InvalidGameError
from apps.flask.websocktoe import const as C


__docformat__ = 'restructuredtext en'


def get_game(id):
    """Gets :class:`~ttt.Game` instance for game ``id``

    ``id``
        Game ID of saved game.
    """
    try:
        return ttt.Game(id=id)
    except InvalidGameError as e:
        return None


def marvmin_msg_generator(msg_pool=C.MARVMIN_MSG_POOL):
    """Generates a MarvMin msg from a randomized message pool

    ``msg_pool``
        List of stings to be be shuffled and endlessly iterated by generator
    """
    messages = random.sample(msg_pool, len(msg_pool))
    while True:
        for msg in messages:
            yield msg