# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import fields

from uuidfield import UUIDField


__docformat__ = 'restructuredtext en'


class TicTacToeMoveModel(models.Model):
    """Provides move node model for building a move tree and looking up moves
    """
    player = fields.CharField(verbose_name="Player",
        null=False, blank=False, db_index=True, max_length=1)
    prev_board = fields.IntegerField(verbose_name="Previous Board State",
        null=False, blank=False, db_index=True)
    move = fields.SmallIntegerField(verbose_name="Move",
         null=False, blank=False, db_index=True)


class TicTacToeGameModel(models.Model):
    """Provides a game model for persisting game state.
    """
    gid = UUIDField(verbose_name="Game ID",
        null=False, blank=False, auto=True)
    board = fields.IntegerField(verbose_name="Board State",
        null=True, blank=True)
    turn = fields.CharField(verbose_name="Player's Turn",
        null=True, blank=True, max_length=1)