# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Country'
        db.create_table(u'crm_country', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=192, blank=True)),
            ('iso_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=6, blank=True)),
            ('developing', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'crm', ['Country'])

        # Adding model 'Organization'
        db.create_table(u'crm_organization', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('legal_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.CharField')(default='', unique=True, max_length=30)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('membership_type', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
            ('membership_status', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
            ('associate_consortium', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('crmid', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('main_website', self.gf('django.db.models.fields.TextField')(max_length=255, blank=True)),
            ('ocw_website', self.gf('django.db.models.fields.TextField')(max_length=255, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('logo_large', self.gf('django.db.models.fields.files.ImageField')(max_length=255, blank=True)),
            ('logo_small', self.gf('django.db.models.fields.files.ImageField')(max_length=255, blank=True)),
            ('rss_course_feed', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('accreditation_body', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('support_commitment', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('ocw_contact', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ocw_contact_user', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal(u'crm', ['Organization'])

        # Adding model 'Contact'
        db.create_table(u'crm_contact', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Organization'])),
            ('contact_type', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=255)),
            ('first_name', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('job_title', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
        ))
        db.send_create_signal(u'crm', ['Contact'])

        # Adding model 'Address'
        db.create_table(u'crm_address', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Organization'])),
            ('street_address', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('supplemental_address_1', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('supplemental_address_2', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('postal_code_suffix', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('state_province', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('state_province_abbr', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Country'], null=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'crm', ['Address'])

        # Adding model 'MembershipApplication'
        db.create_table(u'crm_membershipapplication', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Organization'], null=True, blank=True)),
            ('membership_type', self.gf('django.db.models.fields.IntegerField')(default=None, max_length=10, null=True, blank=True)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('edit_link_key', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('view_link_key', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('legacy_application_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('legacy_entity_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('main_website', self.gf('django.db.models.fields.CharField')(max_length=765, blank=True)),
            ('ocw_website', self.gf('django.db.models.fields.CharField')(max_length=765, blank=True)),
            ('logo_large', self.gf('django.db.models.fields.CharField')(max_length=765, blank=True)),
            ('logo_small', self.gf('django.db.models.fields.CharField')(max_length=765, blank=True)),
            ('institution_country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Country'], null=True, blank=True)),
            ('rss_course_feed', self.gf('django.db.models.fields.CharField')(max_length=765, blank=True)),
            ('rss_referral_link', self.gf('django.db.models.fields.CharField')(max_length=765, blank=True)),
            ('rss_course_feed_language', self.gf('django.db.models.fields.CharField')(max_length=765, blank=True)),
            ('agreed_to_terms', self.gf('django.db.models.fields.CharField')(max_length=765, blank=True)),
            ('agreed_criteria', self.gf('django.db.models.fields.CharField')(max_length=765, blank=True)),
            ('contract_version', self.gf('django.db.models.fields.CharField')(max_length=765, blank=True)),
            ('ocw_software_platform', self.gf('django.db.models.fields.CharField')(max_length=765, blank=True)),
            ('ocw_platform_details', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('ocw_site_hosting', self.gf('django.db.models.fields.CharField')(max_length=765, blank=True)),
            ('ocw_site_approved', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('ocw_published_languages', self.gf('django.db.models.fields.CharField')(max_length=765, blank=True)),
            ('ocw_license', self.gf('django.db.models.fields.CharField')(max_length=765, blank=True)),
            ('organization_type', self.gf('django.db.models.fields.CharField')(max_length=765, blank=True)),
            ('is_accredited', self.gf('django.db.models.fields.NullBooleanField')(default=None, null=True, blank=True)),
            ('accreditation_body', self.gf('django.db.models.fields.CharField')(default='', max_length=765, blank=True)),
            ('ocw_launch_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('support_commitment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('app_status', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('street_address', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('supplemental_address_1', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('supplemental_address_2', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('state_province', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='app_country', null=True, to=orm['crm.Country'])),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=255, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('job_title', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('simplified_membership_type', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('corporate_support_levels', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('associate_consortium', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('moa_terms', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('terms_of_use', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('coppa', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'crm', ['MembershipApplication'])

        # Adding model 'MembershipApplicationComment'
        db.create_table(u'crm_membershipapplicationcomment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.MembershipApplication'])),
            ('legacy_comment_id', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('legacy_app_id', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('sent_email', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('app_status', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'crm', ['MembershipApplicationComment'])

        # Adding model 'ReportedStatistic'
        db.create_table(u'crm_reportedstatistic', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Organization'])),
            ('report_month', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('report_year', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('site_visits', self.gf('django.db.models.fields.IntegerField')()),
            ('orig_courses', self.gf('django.db.models.fields.IntegerField')()),
            ('trans_courses', self.gf('django.db.models.fields.IntegerField')()),
            ('orig_course_lang', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('trans_course_lang', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('oer_resources', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('trans_oer_resources', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('report_date', self.gf('django.db.models.fields.DateField')()),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('carry_forward', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'crm', ['ReportedStatistic'])


    def backwards(self, orm):
        
        # Deleting model 'Country'
        db.delete_table(u'crm_country')

        # Deleting model 'Organization'
        db.delete_table(u'crm_organization')

        # Deleting model 'Contact'
        db.delete_table(u'crm_contact')

        # Deleting model 'Address'
        db.delete_table(u'crm_address')

        # Deleting model 'MembershipApplication'
        db.delete_table(u'crm_membershipapplication')

        # Deleting model 'MembershipApplicationComment'
        db.delete_table(u'crm_membershipapplicationcomment')

        # Deleting model 'ReportedStatistic'
        db.delete_table(u'crm_reportedstatistic')


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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 12, 19, 22, 20, 14, 750931)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 12, 19, 22, 20, 14, 750549)'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'crm.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['crm.Country']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['crm.Organization']"}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'postal_code_suffix': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'state_province': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'state_province_abbr': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'street_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'supplemental_address_1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'supplemental_address_2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'crm.contact': {
            'Meta': {'object_name': 'Contact'},
            'contact_type': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            'first_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['crm.Organization']"})
        },
        u'crm.country': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Country'},
            'developing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '6', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '192', 'blank': 'True'})
        },
        u'crm.membershipapplication': {
            'Meta': {'object_name': 'MembershipApplication'},
            'accreditation_body': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '765', 'blank': 'True'}),
            'agreed_criteria': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'}),
            'agreed_to_terms': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'}),
            'app_status': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'associate_consortium': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'contract_version': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'}),
            'coppa': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'corporate_support_levels': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'app_country'", 'null': 'True', 'to': u"orm['crm.Country']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'edit_link_key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution_country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['crm.Country']", 'null': 'True', 'blank': 'True'}),
            'is_accredited': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'job_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'legacy_application_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'legacy_entity_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'logo_large': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'}),
            'logo_small': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'}),
            'main_website': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'}),
            'membership_type': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'moa_terms': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'ocw_launch_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'ocw_license': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'}),
            'ocw_platform_details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'ocw_published_languages': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'}),
            'ocw_site_approved': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'ocw_site_hosting': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'}),
            'ocw_software_platform': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'}),
            'ocw_website': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['crm.Organization']", 'null': 'True', 'blank': 'True'}),
            'organization_type': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'rss_course_feed': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'}),
            'rss_course_feed_language': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'}),
            'rss_referral_link': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'}),
            'simplified_membership_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'state_province': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'street_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'supplemental_address_1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'supplemental_address_2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'support_commitment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'terms_of_use': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'view_link_key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'crm.membershipapplicationcomment': {
            'Meta': {'object_name': 'MembershipApplicationComment'},
            'app_status': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['crm.MembershipApplication']"}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legacy_app_id': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'legacy_comment_id': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'sent_email': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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
        u'crm.reportedstatistic': {
            'Meta': {'object_name': 'ReportedStatistic'},
            'carry_forward': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {}),
            'oer_resources': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['crm.Organization']"}),
            'orig_course_lang': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'orig_courses': ('django.db.models.fields.IntegerField', [], {}),
            'report_date': ('django.db.models.fields.DateField', [], {}),
            'report_month': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'report_year': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'site_visits': ('django.db.models.fields.IntegerField', [], {}),
            'trans_course_lang': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'trans_courses': ('django.db.models.fields.IntegerField', [], {}),
            'trans_oer_resources': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['crm']
