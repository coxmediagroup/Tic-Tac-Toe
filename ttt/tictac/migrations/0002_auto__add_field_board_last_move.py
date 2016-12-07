# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Board.last_move'
        db.add_column(u'tictac_board', 'last_move',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Board.last_move'
        db.delete_column(u'tictac_board', 'last_move')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'tictac.board': {
            'Meta': {'object_name': 'Board'},
            'columns': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_move': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rows': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'tictac.game': {
            'Meta': {'object_name': 'Game'},
            'board': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tictac.Board']"}),
            'date_started': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'game_over': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'game_type': ('django.db.models.fields.CharField', [], {'default': "'classic'", 'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_play': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'players': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'players'", 'symmetrical': 'False', 'through': u"orm['tictac.GamePlayers']", 'to': u"orm['tictac.Player']"}),
            'turn_counter': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'games_won'", 'null': 'True', 'to': u"orm['tictac.Player']"})
        },
        u'tictac.gameplayers': {
            'Meta': {'object_name': 'GamePlayers'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tictac.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tictac.Player']"}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '8'})
        },
        u'tictac.player': {
            'Meta': {'object_name': 'Player', '_ormbases': [u'auth.User']},
            'ai': ('django.db.models.fields.CharField', [], {'default': "'boehner'", 'max_length': '64'}),
            'auto': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['tictac']