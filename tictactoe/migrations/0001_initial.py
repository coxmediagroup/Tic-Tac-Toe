# -*- coding: utf-8 -*-
# flake8: noqa
# pylint: disable=line-too-long, invalid-name, missing-docstring, unused-argument, no-self-use
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Game'
        db.create_table(u'tictactoe_game', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('server_player', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('winner', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('strategy_type', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'tictactoe', ['Game'])


    def backwards(self, orm):
        # Deleting model 'Game'
        db.delete_table(u'tictactoe_game')


    models = {
        u'tictactoe.game': {
            'Meta': {'object_name': 'Game'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'server_player': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'state': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'strategy_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'winner': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['tictactoe']
