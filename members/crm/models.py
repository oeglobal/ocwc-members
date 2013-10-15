from django.db import models
from django.utils.text import slugify
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
import reversion

class Country(models.Model):
    name = models.CharField(max_length=192, unique=True, blank=True)
    iso_code = models.CharField(max_length=6, unique=True, blank=True)
    developing = models.BooleanField()

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
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
    (18, 'Nominating Committee')
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
    ('UNIVERSIA', 'UNIVERSIA')
)

class ActiveOrganizationManager(models.Manager):
    def get_query_set(self):
        return super(ActiveOrganizationManager, self).get_query_set().filter(membership_status__in=(2,3,7)).order_by('display_name')

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

reversion.register(Address)

APPLICATION_MEMBERSHIP_TYPE = (

)

APPLICATION_STATUS_CHOICES = (
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

class MembershipApplication(models.Model):
    organization = models.ForeignKey(Organization, blank=True, null=True)
    membership_type = models.IntegerField(max_length=10, choices=ORGANIZATION_MEMBERSHIP_TYPE_CHOICES)

    display_name = models.CharField(max_length=255, blank=True, verbose_name="Institution Name")
    access_link_key = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    legacy_application_id = models.IntegerField(blank=True, null=True)
    legacy_entity_id = models.IntegerField()

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

    is_accredited = models.NullBooleanField(default=None)
    accreditation_body = models.CharField(max_length=765, blank=True, default='')
    ocw_launch_date = models.DateTimeField(null=True, blank=True)   

    support_commitment = models.TextField(blank=True)

    app_status = models.CharField(choices=APPLICATION_STATUS_CHOICES, max_length=255)
    created = models.DateTimeField() #auto_now_add=True
    modified = models.DateTimeField() #auto_now=True

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