# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Game.winner'
        db.add_column(u'tictactoe_game', 'winner',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=1, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Game.winner'
        db.delete_column(u'tictactoe_game', 'winner')


    models = {
        u'tictactoe.game': {
            'Meta': {'object_name': 'Game'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'player': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'winner': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'})
        },
        u'tictactoe.move': {
            'Meta': {'ordering': "['created']", 'unique_together': "(('game', 'cell'),)", 'object_name': 'Move'},
            'cell': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'moves'", 'to': u"orm['tictactoe.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['tictactoe']