import uuid
import datetime

from django.db import models
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
import reversion
from geopy import geocoders
from geopy.geocoders.google import GQueryError

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
    (6 , 'Organizational Members'),
    (7 , 'Associate Consortium Members'),
    (8 , 'Corporate Members - Basic'),
    (9 , 'Associate Institutional Members'),
    (10, 'Institutional Members - MRC'),
    (11, 'Institutional Members - DC'),
    (12, 'Institutional Members - DC - MRC'),
    (13, 'Organizational Members - DC'),
    (14, 'Associate Consortium Members - DC'),
    (15, 'Corporate Members - Premium'),
    (16, 'Corporate Members - Sustaining'),
    (17, 'Associate Institutional Members - DC'),
    (18, 'Nominating Committee'),
    (19, 'Organizational Members - DC - MRC'),
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
    ('FOCW', 'OCW France')
)

class ActiveOrganizationManager(models.Manager):
    def get_query_set(self):
        return super(ActiveOrganizationManager, self).get_query_set().filter(membership_status__in=(2,3,5,7)).order_by('display_name')

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

    ocw_contact = models.ForeignKey(User, null=True, verbose_name=u'Primary contact inside OCW', related_name='ocw_contact_user')

    objects = models.Manager()
    active = ActiveOrganizationManager()

    def __unicode__(self):
        return self.display_name

    def get_absolute_staff_url(self):
        return reverse('staff:organization-view', kwargs={'pk':self.id})

    def get_absolute_url(self):
        return reverse('crm:organization-view', kwargs={'pk':self.id})

    def save(self, force_insert=False, force_update=False, using=None):
        if not self.slug:
            slug = slugify(self.display_name)[:30]
            if Organization.objects.filter(slug=slug).exists():
                slug = slug[:29] + '2'
            self.slug = slug

        super(Organization, self).save(force_insert=force_insert, force_update=force_update, using=using)

reversion.register(Organization)

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
reversion.register(Contact)

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

            place, (lat, lng) = g.geocode(address_string)
            
            if lat:
                self.latitude = lat
                self.longitude = lng

        super(Address, self).save(force_insert=force_insert, force_update=force_update, using=using)


reversion.register(Address)

APPLICATION_MEMBERSHIP_TYPE = (

)

APPLICATION_STATUS_CHOICES = (
    ('Submitted', 'Submitted'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
    ('Spam', 'Spam'),
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
    organization = models.ForeignKey(Organization, blank=True, null=True)
    membership_type = models.IntegerField(max_length=10, choices=ORGANIZATION_MEMBERSHIP_TYPE_CHOICES, blank=True, null=True, default=None)

    display_name = models.CharField(max_length=255, blank=True, verbose_name="Institution Name")
    
    edit_link_key = models.CharField(max_length=255, blank=True)
    view_link_key = models.CharField(max_length=255, blank=True)

    description = models.TextField(blank=True)

    legacy_application_id = models.IntegerField(blank=True, null=True)
    legacy_entity_id = models.IntegerField(blank=True, null=True)

    main_website = models.CharField(max_length=765, blank=True, verbose_name=u'Main Website address')
    ocw_website = models.CharField(max_length=765, blank=True, verbose_name=u'OCW Website address')

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
                self.edit_link_key = uuid.uuid4()

        if not self.view_link_key:
            self.view_link_key = uuid.uuid4()

        if not self.modified:
            self.modified = datetime.datetime.now()
        if not self.created:
            self.created = datetime.datetime.now()

        if not self.app_status:
            self.app_status = 'Submitted'

        if self.app_status == 'Approved' and not self.organization:
            self.organization = self._create_member()

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

    report_date = models.DateField()
    last_modified = models.DateTimeField()
    carry_forward = models.BooleanField()

    def get_absolute_url(self):
        return reverse('crm:reported-statistics-view', kwargs={'pk':self.organization.id})