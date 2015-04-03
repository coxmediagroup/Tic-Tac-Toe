# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Game'
        db.create_table(u'game_game', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('board', self.gf('django.db.models.fields.CharField')(default='         ', max_length=9)),
            ('player_x', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('player_o', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'game', ['Game'])


    def backwards(self, orm):
        # Deleting model 'Game'
        db.delete_table(u'game_game')


    models = {
        u'game.game': {
            'Meta': {'object_name': 'Game'},
            'board': ('django.db.models.fields.CharField', [], {'default': "'         '", 'max_length': '9'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player_o': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'player_x': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['game']