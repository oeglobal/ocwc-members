# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'ConferenceRegistration.interface'
        db.add_column(u'conferences_conferenceregistration', 'interface', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['conferences.ConferenceInterface']), keep_default=False)

        # Adding field 'ConferenceRegistration.form_id'
        db.add_column(u'conferences_conferenceregistration', 'form_id', self.gf('django.db.models.fields.CharField')(default=1, max_length=255), keep_default=False)

        # Adding field 'ConferenceRegistration.entry_id'
        db.add_column(u'conferences_conferenceregistration', 'entry_id', self.gf('django.db.models.fields.CharField')(default=1, max_length=255), keep_default=False)

        # Adding field 'ConferenceRegistration.ticket_type'
        db.add_column(u'conferences_conferenceregistration', 'ticket_type', self.gf('django.db.models.fields.CharField')(default='paypal', max_length=255), keep_default=False)

        # Adding field 'ConferenceRegistration.total_amount'
        db.add_column(u'conferences_conferenceregistration', 'total_amount', self.gf('django.db.models.fields.CharField')(default=0, max_length=255), keep_default=False)

        # Adding field 'ConferenceRegistration.payment_type'
        db.add_column(u'conferences_conferenceregistration', 'payment_type', self.gf('django.db.models.fields.CharField')(default='ticket', max_length=255), keep_default=False)

        # Adding field 'ConferenceRegistration.source_url'
        db.add_column(u'conferences_conferenceregistration', 'source_url', self.gf('django.db.models.fields.CharField')(default='', max_length=255), keep_default=False)

        # Adding field 'ConferenceRegistration.last_synced'
        db.add_column(u'conferences_conferenceregistration', 'last_synced', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.date(2016, 9, 5), blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'ConferenceRegistration.interface'
        db.delete_column(u'conferences_conferenceregistration', 'interface_id')

        # Deleting field 'ConferenceRegistration.form_id'
        db.delete_column(u'conferences_conferenceregistration', 'form_id')

        # Deleting field 'ConferenceRegistration.entry_id'
        db.delete_column(u'conferences_conferenceregistration', 'entry_id')

        # Deleting field 'ConferenceRegistration.ticket_type'
        db.delete_column(u'conferences_conferenceregistration', 'ticket_type')

        # Deleting field 'ConferenceRegistration.total_amount'
        db.delete_column(u'conferences_conferenceregistration', 'total_amount')

        # Deleting field 'ConferenceRegistration.payment_type'
        db.delete_column(u'conferences_conferenceregistration', 'payment_type')

        # Deleting field 'ConferenceRegistration.source_url'
        db.delete_column(u'conferences_conferenceregistration', 'source_url')

        # Deleting field 'ConferenceRegistration.last_synced'
        db.delete_column(u'conferences_conferenceregistration', 'last_synced')


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
            'entry_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'form_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interface': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['conferences.ConferenceInterface']"}),
            'last_synced': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'payment_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'source_url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ticket_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'total_amount': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['conferences']
