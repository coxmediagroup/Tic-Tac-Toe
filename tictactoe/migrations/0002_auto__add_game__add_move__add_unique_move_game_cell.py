# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Game'
        db.create_table(u'tictactoe_game', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('player', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('ip', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
        ))
        db.send_create_signal(u'tictactoe', ['Game'])

        # Adding model 'Move'
        db.create_table(u'tictactoe_move', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(related_name='moves', to=orm['tictactoe.Game'])),
            ('cell', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal(u'tictactoe', ['Move'])

        # Adding unique constraint on 'Move', fields ['game', 'cell']
        db.create_unique(u'tictactoe_move', ['game_id', 'cell'])


    def backwards(self, orm):
        # Removing unique constraint on 'Move', fields ['game', 'cell']
        db.delete_unique(u'tictactoe_move', ['game_id', 'cell'])

        # Deleting model 'Game'
        db.delete_table(u'tictactoe_game')

        # Deleting model 'Move'
        db.delete_table(u'tictactoe_move')


    models = {
        u'tictactoe.game': {
            'Meta': {'object_name': 'Game'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'player': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'tictactoe.move': {
            'Meta': {'unique_together': "(('game', 'cell'),)", 'object_name': 'Move'},
            'cell': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'moves'", 'to': u"orm['tictactoe.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['tictactoe']