# -*- coding: utf-8 -*-
import os
import sys
import uuid
import subprocess
import tempfile
import datetime
import time

from django.db import models
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.conf import settings

from geopy import geocoders
from geopy.geocoders.google import GQueryError

# import reversion
here = lambda x: os.path.join(os.path.dirname(os.path.abspath(__file__)), x)

class Country(models.Model):
    name = models.CharField(max_length=192, unique=True, blank=True)
    iso_code = models.CharField(max_length=6, unique=True, blank=True)
    developing = models.BooleanField()

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        if self.developing:
            return self.name + " (D)"
        return self.name

ORGANIZATION_MEMBERSHIP_TYPE_CHOICES = (
    (5 , 'Institutional Members'),
    (10, 'Institutional Members - MRC'),
    (11, 'Institutional Members - DC'),
    (12, 'Institutional Members - DC - MRC'),

    (9 , 'Associate Institutional Members'),
    (17, 'Associate Institutional Members - DC'),

    (6 , 'Organizational Members'),
    (13, 'Organizational Members - DC'),
    (18, 'Organizational Members - MRC'),

    (7 , 'Associate Consortium Members'),
    (14, 'Associate Consortium Members - DC'),

    (8 , 'Corporate Members - Basic'),    
    (15, 'Corporate Members - Premium'),
    (16, 'Corporate Members - Sustaining'),
    
)

ORGANIZATION_TYPE_CHOICES = (
    ('university', 'Higher Education Institution'),
    ('npo', 'Non-Profit Organization'),
    ('ngo', 'Non-Governmental Organization'),
    ('regionalconsortium', 'Regional Consortium'),
    ('software', 'Software Development'),
    ('commercial', 'Commercial Entity')
)

ORGANIZATION_MEMBERSHIP_STATUS = (
    (1, 'Applied'),
    (2, 'Current'),
    (3, 'Grace'),
    (4, 'Expired'),
    (5, 'Pending'),
    (6, 'Cancelled'),
    (7, 'Sustaining'),
    # (8,   'Deceased'),
    # (9,   'Testing'),
    # (10,'Committee'),
    # (11,'Committee'),
    # (12,'Suspended'),
    # (13,'New'),
    (99,'Example')
)

ORGANIZATION_ASSOCIATED_CONSORTIUM = (
    ('CCCOER', 'Community College Consortium for Open Educational Resources (CCCOER)'),
    ('CORE', 'CORE'),
    ('JOCWC', 'Japan OCW Consortium'),
    ('KOCWC', 'Korea OCW Consortium'),
    ('TOCWC', 'Taiwan OpenCourseWare Consortium'),
    ('Turkish OCWC', 'Turkish OpenCourseWare Consortium'),
    ('UNIVERSIA', 'UNIVERSIA'),
    ('FOCW', 'OCW France'),
    ('OTHER', 'OTHER')
)

class ActiveOrganizationManager(models.Manager):
    def get_query_set(self):
        return super(ActiveOrganizationManager, self).get_query_set().filter(membership_status__in=(2,3,5,7,99)).order_by('display_name')

class Organization(models.Model):
    legal_name = models.CharField(max_length=255, blank=True)
    display_name = models.CharField(max_length=255, verbose_name="Name of the organization")
    slug = models.CharField(max_length=30, unique=True, default='')
    user = models.ForeignKey(User, blank=True, null=True)

    membership_type = models.IntegerField(max_length=10, choices=ORGANIZATION_MEMBERSHIP_TYPE_CHOICES)
    # organization_type = models.CharField(max_length=255, choices=ORGANIZATION_TYPE_CHOICES)
    membership_status = models.IntegerField(max_length=10, choices=ORGANIZATION_MEMBERSHIP_STATUS)
    associate_consortium = models.CharField(max_length=255, choices=ORGANIZATION_ASSOCIATED_CONSORTIUM, blank=True, default='')

    crmid = models.CharField(max_length=255, blank=True, help_text='Legacy identifier')

    main_website = models.TextField(max_length=255, blank=True)
    ocw_website = models.TextField(max_length=255, blank=True, verbose_name="OCW Website")

    description = models.TextField(blank=True)
    logo_large = models.ImageField(max_length=255, upload_to="logos", blank=True)
    logo_small = models.ImageField(max_length=255, upload_to="logos", blank=True)
    rss_course_feed = models.CharField(max_length=255, blank=True)

    accreditation_body = models.CharField(max_length=255, blank=True, default='')
    support_commitment = models.TextField(blank=True, default='')

    ocw_contact = models.ForeignKey(User, null=True, verbose_name=u'Primary contact inside OCW', related_name='ocw_contact_user',
                                    limit_choices_to={'is_staff': True})

    objects = models.Manager()
    active = ActiveOrganizationManager()

    def __unicode__(self):
        return self.display_name

    def get_absolute_staff_url(self):
        return reverse('staff:organization-view', kwargs={'pk':self.id})

    def get_absolute_url(self):
        return reverse('crm:organization-view', kwargs={'pk':self.id})

    def get_logo_small_url(self):
        return 'http://www.oeconsortium.org/media/%s' % self.logo_small

    def save(self, force_insert=False, force_update=False, using=None):
        if not self.slug:
            slug = slugify(self.display_name)[:30]
            if Organization.objects.filter(slug=slug).exists():
                slug = slug[:29] + '2'
            self.slug = slug

        super(Organization, self).save(force_insert=force_insert, force_update=force_update, using=using)

    def get_membership_due_amount(self):
        # Sustaining members
        if self.membership_status in [7]:
            return 0    #manually processed

        # (8 , 'Corporate Members - Basic'),    
        if self.membership_type in [8]:
            return 1000

        # (5 , 'Institutional Members'),
        # (6 , 'Organizational Members'),
        # (11, 'Institutional Members - DC'),
        # (7 , 'Associate Consortium Members'),
        # (13, 'Organizational Members - DC'),
        if self.membership_type in [5,6,11,7,13]:
            if self.address_set.latest('id').country.developing:
                return 375
            else:
                return 750

        # (10, 'Institutional Members - MRC'),
        # (12, 'Institutional Members - DC - MRC'),
        # (9 , 'Associate Institutional Members'),
        # (17, 'Associate Institutional Members - DC')
        # (14, 'Associate Consortium Members - DC'),
        # (18, 'Organizational Members - MRC'),
        if self.membership_type in [10, 12, 9, 17, 14]:
            if self.address_set.latest('id').country.developing:
                return 225
            else:
                return 525

    def get_invoice_status(self):
        return {
            'create_invoice': self.billinglog_set.filter(log_type='create_invoice', invoice_year=settings.DEFAULT_INVOICE_YEAR).exists(),
            'send_invoice': self.billinglog_set.filter(log_type='send_invoice', invoice_year=settings.DEFAULT_INVOICE_YEAR).exists(),
        }

    def get_consortia_members(self):

        consortia = None
        if self.slug == 'cccoer':
            consortia = 'CCCOER'
        elif self.slug == 'japan-ocw-consortium':
            consortia = 'JOCWC'
        elif self.slug == 'korea-ocw-consortium':
            consortia = 'KOCWC'
        elif self.slug == 'taiwan-ocw-consortium':
            consortia = 'TOCWC'
        elif self.slug == 'turkish-ocw-consortium':
            consortia = 'Turkish OCWC'
        elif self.slug == 'taiwan-ocw-consortium':
            consortia = 'TOCWC'
        elif self.slug == 'universia':
            consortia = 'UNIVERSIA'
        elif self.slug == 'ocwfrance':
            consortia = 'FOCW'

        if not consortia:
            return Organization.objects.none()

        return Organization.objects.filter(associate_consortium=consortia)

    def can_vote(self):
        if self.membership_status in (2, 5, 7, 99):  # exclude grace (3) from voting
            return True
        else:
            return False

    def get_number_of_votes(self):
        # if len(self.get_consortia_members()) > 30:
        #     return 5
        # elif len(self.get_consortia_members()) > 20:
        #     return 4
        # elif len(self.get_consortia_members()) > 10:
        #     return 3
        # elif len(self.get_consortia_members()) > 1:
        #     return 2

        return 1

    def get_bouncing_contacts(self):
        return self.contact_set.filter(bouncing=True)

    def get_simplified_membership(self):
        text = self.get_membership_type_display()
        text = text.replace('- MRC', '').replace('- DC', '').strip()
        return text

# reversion.register(Organization)

# CONTACT_TYPE_CHOICES = (
#   ('lead', 'Main contact'),
#   ('tech', 'Technical contact'),
#   ('billing', 'Billing contact')
# )

CONTACT_TYPE_CHOICES = (
    (4,  'Employee of'),
    (6,  'Lead Contact for'),
    (9,  'Certifier for'),
    (10, 'Voting Representative'),
    (11, 'Affiliated with'),
    (12, 'AC Member of'),
)

class Contact(models.Model):
    organization = models.ForeignKey(Organization)

    contact_type = models.IntegerField(max_length=10, choices=CONTACT_TYPE_CHOICES)
    email = models.EmailField(max_length=255)

    first_name = models.CharField(max_length=255, blank=True, default='')
    last_name = models.CharField(max_length=255, blank=True, default='')
    job_title = models.CharField(max_length=255, blank=True, default='')

    bouncing = models.BooleanField(default=False)
# reversion.register(Contact)

class Address(models.Model):
    organization = models.ForeignKey(Organization)

    street_address = models.CharField(max_length=255, blank=True, help_text='Street address with street number')
    supplemental_address_1 = models.CharField(max_length=255, blank=True)
    supplemental_address_2 = models.CharField(max_length=255, blank=True)

    city = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=50, blank=True)
    postal_code_suffix = models.CharField(max_length=255, blank=True)

    state_province = models.CharField(max_length=255, blank=True)
    state_province_abbr = models.CharField(max_length=255, blank=True)

    country = models.ForeignKey(Country, blank=True, null=True)

    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __unicode__(self):
        return u"%s %s %s" % (self.country.name, self.city, self.street_address)

    def save(self, force_insert=False, force_update=False, using=None):
        if not (self.latitude and self.longitude):
            g = geocoders.GoogleV3()

            address_string = u"%s, %s, %s, %s %s, %s, %s" % (
                             self.street_address, self.supplemental_address_1, self.supplemental_address_2,
                             self.postal_code, self.postal_code_suffix,
                             self.state_province, self.country.name)
            try:
                place, (lat, lng) = g.geocode(address_string)

                if lat:
                    self.latitude = lat
                    self.longitude = lng
            except:
                pass

        super(Address, self).save(force_insert=force_insert, force_update=force_update, using=using)

    def get_absolute_url(self):
        return self.organization.get_absolute_url()


# reversion.register(Address)

APPLICATION_MEMBERSHIP_TYPE = (

)

APPLICATION_STATUS_CHOICES = (
    ('Submitted', 'Submitted'),
    ('Committee', 'Sent to Committee'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
    ('Spam', 'Spam'),
    ('RequestedMoreInfo', 'Requested more information'),
)

ORGANIZATION_TYPE_CHOICES = (
    ('university', 'Higher Education Institution'),
    ('npo', 'Non-Profit Organization'),
    ('ngo', 'Non-Governmental Organization'),
    ('regionalconsortium', 'Regional Consortium'),
    ('software', 'Software Development'),
    ('commercial', 'Commercial Entity'),
)

SIMPLIFIED_MEMBERSHIP_TYPE_CHOICES = (
    ('institutional', 'Institutional Member'),
    ('associate', 'Associate Consortium Member'),
    ('organizational', 'Organizational Member'),
    ('corporate', 'Corporate Member')
)

CORPORATE_SUPPORT_CHOICES = (
    ('basic', 'Basic - $1,000 annual membership fee'),
    # ('premium', 'Premium - $5,000 annual membership fee'),
    ('sustaining', 'Sustaining - $30,000 contribution annual membership fee'),
    ('bronze', 'Bronze - $60,000 contribution annual membership fee'),
    ('silver', 'Silver - $100,000 contribution annual membership fee'),
    ('gold', 'Gold - $150,000 contribution annual membership fee'),
    ('platinum', 'Platinum - $250,000 contribution annual membership fee'),
)

IS_ACCREDITED_CHOICES = (
    (1, 'Yes'),
    (0, 'No'),
)

class MembershipApplication(models.Model):
    organization = models.ForeignKey(Organization, blank=True, null=True, help_text='Should be empty, unless application is approved')
    membership_type = models.IntegerField(max_length=10, choices=ORGANIZATION_MEMBERSHIP_TYPE_CHOICES, blank=True, null=True, default=None)

    display_name = models.CharField(max_length=255, blank=True, verbose_name="Institution Name")

    edit_link_key = models.CharField(max_length=255, blank=True)
    view_link_key = models.CharField(max_length=255, blank=True)

    description = models.TextField(blank=True)

    legacy_application_id = models.IntegerField(blank=True, null=True)
    legacy_entity_id = models.IntegerField(blank=True, null=True)

    main_website = models.CharField(max_length=765, blank=True, verbose_name=u'Main Website address')
    ocw_website = models.CharField(max_length=765, blank=True, verbose_name=u'Open Educational Resources (OER) or OpenCourseWare (OCW) Website')

    logo_large = models.CharField(max_length=765, blank=True)
    logo_small = models.CharField(max_length=765, blank=True)
    institution_country = models.ForeignKey(Country, blank=True, null=True)

    rss_course_feed = models.CharField(max_length=765, blank=True)
    rss_referral_link = models.CharField(max_length=765, blank=True)
    rss_course_feed_language = models.CharField(max_length=765, blank=True)

    agreed_to_terms = models.CharField(max_length=765, blank=True)
    agreed_criteria = models.CharField(max_length=765, blank=True)
    contract_version = models.CharField(max_length=765, blank=True)

    ocw_software_platform = models.CharField(max_length=765, blank=True)
    ocw_platform_details = models.TextField(blank=True)
    ocw_site_hosting = models.CharField(max_length=765, blank=True)
    ocw_site_approved = models.NullBooleanField(null=True, blank=True)
    ocw_published_languages = models.CharField(max_length=765, blank=True)
    ocw_license = models.CharField(max_length=765, blank=True)

    organization_type = models.CharField(max_length=765, blank=True, choices=ORGANIZATION_TYPE_CHOICES)

    is_accredited = models.NullBooleanField(default=None, choices=IS_ACCREDITED_CHOICES)
    accreditation_body = models.CharField(max_length=765, blank=True, default='')
    ocw_launch_date = models.DateTimeField(null=True, blank=True)

    support_commitment = models.TextField(blank=True)

    app_status = models.CharField(choices=APPLICATION_STATUS_CHOICES, max_length=255, blank=True)
    created = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    modified = models.DateTimeField(blank=True) #, null=True, auto_now=True)

    #address
    street_address = models.CharField(max_length=255, blank=True, help_text='Street address with a street number')
    supplemental_address_1 = models.CharField(max_length=255, blank=True, verbose_name=u'Street Address 2')
    supplemental_address_2 = models.CharField(max_length=255, blank=True, verbose_name=u'Street Address 3')

    city = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=50, blank=True)

    state_province = models.CharField(max_length=255, blank=True, verbose_name=u'State/Province')
    country = models.ForeignKey(Country, blank=True, null=True, related_name='app_country')

    email = models.EmailField(max_length=255, blank=True)

    first_name = models.CharField(max_length=255, blank=True, default='')
    last_name = models.CharField(max_length=255, blank=True, default='')
    job_title = models.CharField(max_length=255, blank=True, default='')

    simplified_membership_type = models.CharField(max_length=255, blank=True, choices=SIMPLIFIED_MEMBERSHIP_TYPE_CHOICES)
    corporate_support_levels = models.CharField(max_length=255, blank=True, choices=CORPORATE_SUPPORT_CHOICES)
    associate_consortium = models.CharField(max_length=255, choices=ORGANIZATION_ASSOCIATED_CONSORTIUM, blank=True, default='')

    moa_terms = models.NullBooleanField(null=True)
    terms_of_use = models.NullBooleanField(null=True)
    coppa = models.NullBooleanField(null=True)

    def save(self, force_insert=False, force_update=False, using=None):
        if not self.legacy_application_id:
            if not self.edit_link_key:
                self.edit_link_key = uuid.uuid4().get_hex()

        if not self.view_link_key:
            self.view_link_key = uuid.uuid4().get_hex()

        if not self.modified:
            self.modified = datetime.datetime.now()
        if not self.created:
            self.created = datetime.datetime.now()

        if not self.app_status:
            self.app_status = 'Submitted'

        if self.app_status == 'Approved' and not self.organization:
            self.organization = self._create_member()

        if not self.pk:
            self._send_notification_email()

        super(MembershipApplication, self).save(force_insert=force_insert, force_update=force_update, using=using)

    def get_absolute_url(self):
        # return reverse('crm:application-view', kwargs={'view_link_key':self.view_link_key})
        return '/application/view/%s/' % self.view_link_key

    def __unicode__(self):
        return "Application #%s" % self.id

    def _create_member(self):
        org, is_created = Organization.objects.get_or_create(
            display_name = self.display_name,
            membership_type = self.membership_type,
            defaults = {
                'membership_status': 5, #pending
                'associate_consortium': self.associate_consortium,
                'main_website': self.main_website,
                'ocw_website':  self.ocw_website,
                'description':  self.description,
                'support_commitment': self.support_commitment
            })

        contact, is_created = Contact.objects.get_or_create(
            organization = org,
            contact_type = 6, # Lead contact
            email = self.email,
            defaults = {
                'first_name': self.first_name,
                'last_name': self.last_name
            })

        user, is_created = User.objects.get_or_create(
            username = org.slug,
            email = contact.email
        )

        org.user = user
        org.save()

        address, is_created = Address.objects.get_or_create(
            organization = org,
            street_address = self.street_address,
            defaults = {
                'supplemental_address_1': self.supplemental_address_1,
                'supplemental_address_2': self.supplemental_address_2,

                'city': self.city,
                'postal_code': self.postal_code,
                'state_province': self.state_province,
                'country': self.country
            })

        return org

    def _send_notification_email(self):
        send_mail('New Membership Application: %s' % self.display_name, 'View application: http://members.oeconsortium.org%s' % self.get_absolute_url(), 
                    'tech@oeconsortium.org', ['memberapplications@oeconsortium.org'])

COMMENTS_APP_STATUS_CHOICES = (
    ('Requested More Info', 'Requested More Info'),
    ('Spam', 'Spam'),
    ('Approved', 'Approved')
)

class MembershipApplicationComment(models.Model):
    application = models.ForeignKey(MembershipApplication)

    legacy_comment_id = models.IntegerField(blank=True)
    legacy_app_id = models.IntegerField(blank=True)

    comment = models.TextField(blank=True)
    sent_email = models.BooleanField(default=False)
    app_status = models.CharField(max_length=255, blank=True) #, choices=COMMENTS_APP_STATUS_CHOICES, blank=True)

    created = models.DateTimeField() #auto_now_add=True

class ReportedStatistic(models.Model):
    organization = models.ForeignKey(Organization)
    report_month = models.CharField(max_length=6)
    report_year = models.CharField(max_length=12)
    site_visits = models.IntegerField()
    orig_courses = models.IntegerField(verbose_name=u'Original Courses')
    trans_courses = models.IntegerField(verbose_name=u'Translated Courses')
    orig_course_lang = models.TextField(blank=True, verbose_name=u'Original Courses Language')
    trans_course_lang = models.TextField(blank=True, null=True, verbose_name=u'Translated Courses Language')

    oer_resources = models.IntegerField(null=True, blank=True, verbose_name=u'Number of OER Resources')
    trans_oer_resources = models.IntegerField(null=True, blank=True, verbose_name=u'Number of Translated OER Resources')
    comment = models.TextField(blank=True, null=True, verbose_name=u'Comment')

    report_date = models.DateField(verbose_name=u'Reported period')
    last_modified = models.DateTimeField(auto_now_add=True)
    carry_forward = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('crm:reported-statistics-view', kwargs={'pk':self.organization.id})

class LoginKey(models.Model):
    user = models.ForeignKey(User)
    email = models.EmailField()
    key = models.CharField(max_length=32)

    used = models.BooleanField(default=False)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s - %s" % (self.user, self.email)

    def save(self, force_insert=False, force_update=False, using=None):
        if not self.key:
            self.key = uuid.uuid4().get_hex()

        super(LoginKey, self).save(force_insert=force_insert, force_update=force_update, using=using)

    def send_email(self):
        body = render_to_string('mail-login/mail_body.txt', {'url': self.get_absolute_url()})
        send_mail('OCW Member portal login information', body, 
                    'memberservices@oeconsortium.org', [self.email])

    def get_absolute_url(self):
        return '/login/%s/' % self.key

BILLING_LOG_TYPE_CHOICES = (
    ('create_invoice', 'Create new invoice'),
    ('send_invoice', 'Send invoice via email'),
    ('create_paid_invoice', 'Create paid invoice'),
    ('send_paid_invoice', 'Send paid invoice via email'),
    ('create_note', 'Add a note'),
)

class BillingLog(models.Model):
    log_type = models.CharField(max_length=30, choices=BILLING_LOG_TYPE_CHOICES)
    organization = models.ForeignKey(Organization)
    pub_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    created_date = models.DateField(null=True, verbose_name='Created Date (year-month-day)')

    amount = models.IntegerField(null=True)
    email = models.CharField(max_length=120, blank=True, verbose_name="Recepient email")
    invoice = models.ForeignKey('Invoice', null=True, blank=True)
    invoice_year = models.CharField(default=settings.DEFAULT_INVOICE_YEAR, max_length=10)
    description = models.TextField(blank=True, default='')
    note = models.TextField(blank=True)

    email_subject = models.CharField(max_length=140, blank=True, verbose_name="Subject")
    email_body = models.TextField(blank=True, verbose_name="Message")

    @staticmethod
    def _open_file(path_to_file, attempts=0, timeout=5, sleep_int=5):
        if attempts < timeout and os.path.exists(path_to_file) and os.path.isfile(path_to_file):
            f = open(path_to_file, 'rb')
            return f
        else:
            time.sleep(sleep_int)
            return BillingLog._open_file(path_to_file, attempts + 1)    

    def send_email(self):
        message = EmailMessage(
            subject = self.email_subject,
            body = self.email_body,
            from_email = 'memberservices@oeconsortium.org',
            to = [s.strip() for s in self.email.split(',')],
            bcc = [self.user.email]
        )
        pdf_path = os.path.join(settings.INVOICES_ROOT, self.invoice.pdf_filename)
        
        f = BillingLog._open_file(pdf_path)
        content = f.read()
        f.close()

        message.attach(filename='ocw-invoice-%s.pdf' % self.invoice.invoice_number,
                       content=content, 
                       mimetype='application/pdf')
        message.send()

INVOICE_TYPE_CHOICES = (
    ('issued', 'Normal issued invoice'),
    ('paid', 'Invoice with paid watermark')
)

class Invoice(models.Model):
    invoice_type = models.CharField(max_length=30, default='issued', choices=INVOICE_TYPE_CHOICES)
    organization = models.ForeignKey(Organization)
    invoice_number = models.CharField(max_length=30, blank=True)
    invoice_year = models.CharField(default=settings.DEFAULT_INVOICE_YEAR, max_length=10)
    amount = models.IntegerField()
    description = models.TextField(blank=True)
    
    pdf_filename = models.CharField(max_length=100, blank=True)
    access_key = models.CharField(max_length=32, blank=True)

    created_date = models.DateField(null=True, verbose_name='Created Date (year-month-day)')

    paypal_link = models.TextField(blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "Invoice %s (%s)" % (self.invoice_number, self.organization.display_name)

    def get_absolute_url(self):
        return reverse('staff:invoice-view', kwargs={'pk':self.id})

    def get_access_key_url(self):
        return reverse('staff:invoice-phantomjs-view', kwargs={'access_key':self.access_key})

    def get_pdf_url(self):
        return "%s%s" % (settings.INVOICES_URL, self.pdf_filename)

    def save(self, force_insert=False, force_update=False, using=None):
        if not self.access_key:
            self.access_key = uuid.uuid4().get_hex()
        if not self.paypal_link:
            self.paypal_link = self._get_paypal_link()

        super(Invoice, self).save(force_insert=force_insert, force_update=force_update, using=using)

    def generate_pdf(self):
        url = '%s%s' % (settings.INVOICES_PHANTOM_JS_HOST, self.get_access_key_url())
        filename = "invoice_%s_%s.pdf" % (self.pk, uuid.uuid4().get_hex())
        pdf_path = os.path.join(settings.INVOICES_ROOT, filename)
        
        # print [here('../../bin/phantomjs'), 
        #                   here('phantomjs-scripts/rasterize.js'), 
        #                   url,
        #                   pdf_path,
        #                   'Letter'
        #                 ]

        subprocess.Popen([here('../../bin/phantomjs2'), 
                          here('phantomjs-scripts/rasterize.js'), 
                          url,
                          pdf_path,
                          'Letter'
                        ])

        self.pdf_filename = filename
        self.save()

    def _get_paypal_link(self):
        if self.amount == 225:
            return 'https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=SSS6C5TBMRDJ2'
        if self.amount == 375:
            return 'https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=Y6DLXHCB5E8JL'
        if self.amount == 525:
            return 'https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=HJB7HSG28DC82'
        if self.amount == 750:               
            return 'https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=7LXJWSNC3DPMC'
        if self.amount == 1000:
            return 'https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=Z8THX5FXTWCFS'

        return ''