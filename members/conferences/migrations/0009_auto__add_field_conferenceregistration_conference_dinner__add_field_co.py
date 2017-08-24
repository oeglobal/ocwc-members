# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ConferenceRegistration.conference_dinner'
        db.add_column(u'conferences_conferenceregistration', 'conference_dinner',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)

        # Adding field 'ConferenceRegistration.reception_guest'
        db.add_column(u'conferences_conferenceregistration', 'reception_guest',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ConferenceRegistration.conference_dinner'
        db.delete_column(u'conferences_conferenceregistration', 'conference_dinner')

        # Deleting field 'ConferenceRegistration.reception_guest'
        db.delete_column(u'conferences_conferenceregistration', 'reception_guest')


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
            'access_key': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'billing_address': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'conference_dinner': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'dinner_guest': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
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
            'reception_guest': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'source_url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ticket_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'total_amount': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['conferences']