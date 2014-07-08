# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import json
from flask.json import JSONEncoder

from apps.coxtactoe import tictactoe as ttt


__docformat__ = 'restructuredtext en'


class WebSockToeJSONEncoder(JSONEncoder):
    def default(self, o):
        """Provides JSON encoding support for Game objects."""
        if isinstance(o, ttt.Game):
            if not o.over:
                tied = lost = False
            else:
                tied = True if o.winner is None else False
                lost = True if o.winner == o.player.opponent else False

            return json.dumps({
                'game_id': str(o.id),
                'board': list(o.board),
                'xo_choice': repr(o.player),
                'winner': repr(o.winner),
                'over': o.over,
                'tied': tied,
                'lost': lost,
            })
        return JSONEncoder.default(self, o)


