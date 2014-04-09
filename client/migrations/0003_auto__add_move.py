# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Move'
        db.create_table(u'client_move', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('board', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['client.Game'])),
            ('x_position', self.gf('django.db.models.fields.IntegerField')()),
            ('y_position', self.gf('django.db.models.fields.IntegerField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'client', ['Move'])


    def backwards(self, orm):
        # Deleting model 'Move'
        db.delete_table(u'client_move')


    models = {
        u'client.game': {
            'Meta': {'object_name': 'Game'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'client.move': {
            'Meta': {'object_name': 'Move'},
            'board': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['client.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'x_position': ('django.db.models.fields.IntegerField', [], {}),
            'y_position': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['client']