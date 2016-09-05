# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'ConferenceRegistration.name'
        db.add_column(u'conferences_conferenceregistration', 'name', self.gf('django.db.models.fields.CharField')(default='', max_length=255), keep_default=False)

        # Adding field 'ConferenceRegistration.email'
        db.add_column(u'conferences_conferenceregistration', 'email', self.gf('django.db.models.fields.CharField')(default='', max_length=255), keep_default=False)

        # Adding field 'ConferenceRegistration.organization'
        db.add_column(u'conferences_conferenceregistration', 'organization', self.gf('django.db.models.fields.CharField')(default='', max_length=255), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'ConferenceRegistration.name'
        db.delete_column(u'conferences_conferenceregistration', 'name')

        # Deleting field 'ConferenceRegistration.email'
        db.delete_column(u'conferences_conferenceregistration', 'email')

        # Deleting field 'ConferenceRegistration.organization'
        db.delete_column(u'conferences_conferenceregistration', 'organization')


    models = {
        u'conferences.conferenceinterface': {
            'Meta': {'object_name': 'ConferenceInterface'},
            'api_key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_synced': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'private_key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        u'conferences.conferenceregistration': {
            'Meta': {'object_name': 'ConferenceRegistration'},
            'email': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'entry_created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'entry_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'form_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interface': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['conferences.ConferenceInterface']"}),
            'last_synced': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'organization': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'payment_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'source_url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ticket_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'total_amount': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['conferences']
