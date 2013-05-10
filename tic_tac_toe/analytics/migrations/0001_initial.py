# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Event'
        db.create_table('analytics_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event_type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('event_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('event_model', self.gf('django.db.models.fields.CharField')(default='None', max_length=100)),
            ('event_model_id', self.gf('django.db.models.fields.IntegerField')(default='0')),
            ('event_url', self.gf('django.db.models.fields.CharField')(default='None', max_length=100)),
        ))
        db.send_create_signal('analytics', ['Event'])


    def backwards(self, orm):
        # Deleting model 'Event'
        db.delete_table('analytics_event')


    models = {
        'analytics.event': {
            'Meta': {'ordering': "['event_timestamp']", 'object_name': 'Event'},
            'event_model': ('django.db.models.fields.CharField', [], {'default': "'None'", 'max_length': '100'}),
            'event_model_id': ('django.db.models.fields.IntegerField', [], {'default': "'0'"}),
            'event_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'event_url': ('django.db.models.fields.CharField', [], {'default': "'None'", 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['analytics']