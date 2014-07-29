# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TicTacToeGameModel'
        db.create_table(u'coxtactoe_tictactoegamemodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gid', self.gf('uuidfield.fields.UUIDField')(unique=True, max_length=32, blank=True)),
            ('board', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('turn', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
        ))
        db.send_create_signal(u'coxtactoe', ['TicTacToeGameModel'])


    def backwards(self, orm):
        # Deleting model 'TicTacToeGameModel'
        db.delete_table(u'coxtactoe_tictactoegamemodel')


    models = {
        u'coxtactoe.tictactoegamemodel': {
            'Meta': {'object_name': 'TicTacToeGameModel'},
            'board': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gid': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'turn': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'})
        },
        u'coxtactoe.tictactoemovemodel': {
            'Meta': {'object_name': 'TicTacToeMoveModel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'move': ('django.db.models.fields.SmallIntegerField', [], {'db_index': 'True'}),
            'player': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_index': 'True'}),
            'prev_board': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['coxtactoe']