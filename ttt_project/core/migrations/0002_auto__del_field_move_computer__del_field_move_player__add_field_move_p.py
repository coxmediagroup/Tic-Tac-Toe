# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Move.computer'
        db.delete_column(u'core_move', 'computer')

        # Deleting field 'Move.player'
        db.delete_column(u'core_move', 'player_id')

        # Adding field 'Move.player_move'
        db.add_column(u'core_move', 'player_move',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Move.computer'
        db.add_column(u'core_move', 'computer',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Move.player'
        raise RuntimeError("Cannot reverse this migration. 'Move.player' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Move.player'
        db.add_column(u'core_move', 'player',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']),
                      keep_default=False)

        # Deleting field 'Move.player_move'
        db.delete_column(u'core_move', 'player_move')


    models = {
        u'core.game': {
            'Meta': {'object_name': 'Game'},
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'core.move': {
            'Meta': {'object_name': 'Move'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player_move': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'space': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['core']