# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Election'
        db.create_table(u'elections_election', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('view_nominations_key', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('edit_nominations_key', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'elections', ['Election'])

        # Adding model 'Candidate'
        db.create_table(u'elections_candidate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('election', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elections.Election'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='', max_length=60)),
            ('candidate_first_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('candidate_last_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('candidate_job_title', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('candidate_email', self.gf('django.db.models.fields.EmailField')(max_length=255)),
            ('candidate_phone_number', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('reason', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Organization'])),
            ('sponsor_first_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('sponsor_last_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('sponsor_email', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('edit_link_key', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('view_link_key', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('email_alternate', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('biography', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('vision', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('ideas', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('expertise', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('external_url', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('vetted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('seat_type', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'elections', ['Candidate'])


    def backwards(self, orm):
        
        # Deleting model 'Election'
        db.delete_table(u'elections_election')

        # Deleting model 'Candidate'
        db.delete_table(u'elections_candidate')


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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 2, 5, 13, 38, 49, 403611)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 2, 5, 13, 38, 49, 403236)'}),
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
        u'crm.organization': {
            'Meta': {'object_name': 'Organization'},
            'accreditation_body': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'associate_consortium': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'crmid': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legal_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'logo_large': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'blank': 'True'}),
            'logo_small': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'blank': 'True'}),
            'main_website': ('django.db.models.fields.TextField', [], {'max_length': '255', 'blank': 'True'}),
            'membership_status': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'membership_type': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'ocw_contact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ocw_contact_user'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'ocw_website': ('django.db.models.fields.TextField', [], {'max_length': '255', 'blank': 'True'}),
            'rss_course_feed': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '30'}),
            'support_commitment': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'elections.candidate': {
            'Meta': {'object_name': 'Candidate'},
            'biography': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'candidate_email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            'candidate_first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'candidate_job_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'candidate_last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'candidate_phone_number': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'edit_link_key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'election': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['elections.Election']"}),
            'email_alternate': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'expertise': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'external_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ideas': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['crm.Organization']"}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'reason': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'seat_type': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'sponsor_email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sponsor_first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sponsor_last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '60'}),
            'vetted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'view_link_key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'vision': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'elections.election': {
            'Meta': {'object_name': 'Election'},
            'edit_nominations_key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'view_nominations_key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['elections']
