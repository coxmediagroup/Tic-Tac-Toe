"""
Players are defined their "play" method, which takes a game model
(or an object that proxies a game model, in such a way they aren't
allowed to perform any illegal actions).

They are expected to return an index that is their play.
"""
import random
from django.utils.module_loading import import_by_path


class RandomPlayer(object):
    """
    The random player plays in a random square. It's not very smart.
    """

    def play(self, game):
        # Find a spot on the board that's open.
        open_indexes = [i for i, v in enumerate(game.board) if v == ' ']
        # We probably shouldn't have been called, we can't play!
        if not open_indexes:
            return
        return random.choice(open_indexes)


def get_player(player_type):
    """
    This uses importlib to load the class.
    Since we don't have that many player types, you could hardcode types
    as well.
    """
    cls = import_by_path(player_type)
    return cls()
