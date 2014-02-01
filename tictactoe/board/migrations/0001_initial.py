# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Player'
        db.create_table(u'board_player', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('is_human', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'board', ['Player'])

        # Adding model 'Game'
        db.create_table(u'board_game', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player_1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='player_1', to=orm['board.Player'])),
            ('player_2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='player_2', to=orm['board.Player'])),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_over', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('winner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='winner', null=True, to=orm['board.Player'])),
        ))
        db.send_create_signal(u'board', ['Game'])

        # Adding model 'Move'
        db.create_table(u'board_move', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['board.Game'])),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['board.Player'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('position_x', self.gf('django.db.models.fields.IntegerField')()),
            ('position_y', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'board', ['Move'])

        # Adding unique constraint on 'Move', fields ['game', 'position_x', 'position_y']
        db.create_unique(u'board_move', ['game_id', 'position_x', 'position_y'])


    def backwards(self, orm):
        # Removing unique constraint on 'Move', fields ['game', 'position_x', 'position_y']
        db.delete_unique(u'board_move', ['game_id', 'position_x', 'position_y'])

        # Deleting model 'Player'
        db.delete_table(u'board_player')

        # Deleting model 'Game'
        db.delete_table(u'board_game')

        # Deleting model 'Move'
        db.delete_table(u'board_move')


    models = {
        u'board.game': {
            'Meta': {'object_name': 'Game'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_over': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'player_1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'player_1'", 'to': u"orm['board.Player']"}),
            'player_2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'player_2'", 'to': u"orm['board.Player']"}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'winner'", 'null': 'True', 'to': u"orm['board.Player']"})
        },
        u'board.move': {
            'Meta': {'ordering': "['game', '-time']", 'unique_together': "(('game', 'position_x', 'position_y'),)", 'object_name': 'Move'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['board.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['board.Player']"}),
            'position_x': ('django.db.models.fields.IntegerField', [], {}),
            'position_y': ('django.db.models.fields.IntegerField', [], {}),
            'time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        u'board.player': {
            'Meta': {'object_name': 'Player'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_human': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['board']