# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TicTacToeMoveModel'
        db.create_table(u'coxtactoe_tictactoemovemodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player', self.gf('django.db.models.fields.CharField')(max_length=1, db_index=True)),
            ('prev_board', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('move', self.gf('django.db.models.fields.SmallIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'coxtactoe', ['TicTacToeMoveModel'])


    def backwards(self, orm):
        # Deleting model 'TicTacToeMoveModel'
        db.delete_table(u'coxtactoe_tictactoemovemodel')


    models = {
        u'coxtactoe.tictactoemovemodel': {
            'Meta': {'object_name': 'TicTacToeMoveModel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'move': ('django.db.models.fields.SmallIntegerField', [], {'db_index': 'True'}),
            'player': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_index': 'True'}),
            'prev_board': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['coxtactoe']