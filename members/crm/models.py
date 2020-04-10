# -*- coding: utf-8 -*-
import os
import uuid
import subprocess
import datetime
import time
import random
import arrow

from django.db import models, IntegrityError
from django.db.models.signals import post_save
from django.utils.text import slugify
from django.urls import reverse
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.conf import settings
from django.dispatch import receiver

from quickbooks import Oauth2SessionManager
from quickbooks.objects.base import PhoneNumber, EmailAddress
from quickbooks.objects.base import Address as QuickBooksAddress
from quickbooks.objects.customer import Customer
from quickbooks import QuickBooks
from quickbooks.objects.detailline import SalesItemLine, SalesItemLineDetail
from quickbooks.objects.invoice import Invoice as QuickBooksInvoice
from quickbooks.objects.item import Item
from quickbooks.objects.term import Term
from quickbooks.helpers import qb_date_format

from geopy import geocoders
from .utils import print_pdf

here = lambda x: os.path.join(os.path.dirname(os.path.abspath(__file__)), x)


class Continent(models.Model):
    name = models.CharField(max_length=192, unique=True, blank=True)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=192, unique=True, blank=True)
    iso_code = models.CharField(max_length=6, unique=True, blank=True)
    developing = models.BooleanField()
    continent = models.ForeignKey(Continent, models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


ORGANIZATION_MEMBERSHIP_TYPE_CHOICES = (
    (5, "Institutional Members"),
    (10, "Institutional Members - MRC"),
    (11, "Institutional Members - DC"),
    (12, "Institutional Members - DC - MRC"),
    (9, "Associate Institutional Members"),
    (17, "Associate Institutional Members - DC"),
    (6, "Organizational Members"),
    (13, "Organizational Members - DC"),
    (18, "Organizational Members - MRC"),
    (7, "Associate Consortium Members"),
    (14, "Associate Consortium Members - DC"),
    (8, "Corporate Members - Basic"),
    (15, "Corporate Members - Premium"),
    (16, "Corporate Members - Sustaining"),
)

ORGANIZATION_TYPE_CHOICES = (
    ("university", "Higher Education Institution"),
    ("npo", "Non-Profit Organization"),
    ("ngo", "Non-Governmental Organization"),
    ("regionalconsortium", "Regional Consortium"),
    ("software", "Software Development"),
    ("commercial", "Commercial Entity"),
)

INSTITUTION_TYPE_CHOICES = (
    ("secondary-ed", "Primary and secondary (K-12)"),
    ("college", "Community, technical, or vocational college"),
    ("higher-ed", "University"),
    ("non-accredited", "Informal non-accredited education"),
    ("lifelong", "Lifelong learning"),
    ("consortium", "Consortia Member"),
    ("consortium-org", "Consortia Organization"),
    ("initiative", "Open initiatives or special project"),
    ("commercial", "Corporate enterprise"),
    ("npo", "Non-profits, NGO’s, IGO"),
    ("cultural", "Cultural organization"),
    ("gov", "Government"),
)

ORGANIZATION_MEMBERSHIP_STATUS = (
    (1, "Applied"),
    (2, "Current"),
    (3, "Grace"),
    (4, "Expired"),
    (5, "Pending"),
    (6, "Cancelled"),
    (7, "Sustaining"),
    # (8,   'Deceased'),
    # (9,   'Testing'),
    # (10,'Committee'),
    # (11,'Committee'),
    # (12,'Suspended'),
    # (13,'New'),
    (99, "Example"),
)

ORGANIZATION_ASSOCIATED_CONSORTIUM = (
    ("CCCOER", "Community College Consortium for Open Educational Resources (CCCOER)"),
    ("CORE", "CORE"),
    ("JOCWC", "OE Japan"),
    ("KOCWC", "Korea OCW Consortium"),
    ("TOCEC", "Taiwan Open Course and Education Consortium"),
    ("Turkish OCWC", "Turkish OpenCourseWare Consortium"),
    ("UNIVERSIA", "UNIVERSIA"),
    ("FOCW", "Open Education France"),
    ("OTHER", "OTHER"),
)

ORGANIZATION_BILLING_TYPE = (
    ("normal", "Normal billing"),
    ("consortia", "Billed via Associate Consortia"),
    ("custom", "Custom Agreement"),
    ("waiver", "Fee waiver"),
)


class ActiveOrganizationManager(models.Manager):
    def get_queryset(self):
        return (
            super(ActiveOrganizationManager, self)
            .get_queryset()
            .filter(membership_status__in=(2, 3, 5, 7, 99))
            .order_by("display_name")
        )


class Organization(models.Model):
    legal_name = models.CharField(max_length=255, blank=True)
    display_name = models.CharField(
        max_length=255, verbose_name="Name of the organization"
    )
    slug = models.CharField(max_length=60, unique=True, default="")
    user = models.ForeignKey(User, models.CASCADE, blank=True, null=True)

    membership_type = models.IntegerField(choices=ORGANIZATION_MEMBERSHIP_TYPE_CHOICES)
    # organization_type = models.CharField(max_length=255, choices=ORGANIZATION_TYPE_CHOICES)
    membership_status = models.IntegerField(choices=ORGANIZATION_MEMBERSHIP_STATUS)
    billing_type = models.CharField(
        max_length=128, choices=ORGANIZATION_BILLING_TYPE, default="normal"
    )
    associate_consortium = models.CharField(
        max_length=255,
        choices=ORGANIZATION_ASSOCIATED_CONSORTIUM,
        blank=True,
        default="",
    )

    qbo_id = models.IntegerField(null=True, blank=True, default=None)

    main_website = models.TextField(max_length=255, blank=True)
    ocw_website = models.TextField(
        max_length=255, blank=True, verbose_name="OER/OCW Website"
    )

    description = models.TextField(blank=True)
    logo_large = models.ImageField(max_length=255, upload_to="logos", blank=True)
    logo_small = models.ImageField(max_length=255, upload_to="logos", blank=True)
    rss_course_feed = models.CharField(max_length=255, blank=True)

    accreditation_body = models.CharField(max_length=255, blank=True, default="")
    support_commitment = models.TextField(blank=True, default="")

    ocw_contact = models.ForeignKey(
        User,
        models.CASCADE,
        null=True,
        verbose_name=u"Primary contact inside OCW",
        related_name="ocw_contact_user",
        limit_choices_to={"is_staff": True},
    )

    created = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    institution_type = models.CharField(
        max_length=25, blank=True, choices=INSTITUTION_TYPE_CHOICES, default=""
    )

    initiative_title1 = models.CharField(
        max_length=255, blank=True, default="", verbose_name="Initiative 1 Title"
    )
    initiative_description1 = models.TextField(
        blank=True,
        default="",
        verbose_name="Initiative 1 Description (100 – 350 characters)",
    )
    initiative_url1 = models.URLField(
        max_length=255, blank=True, default="", verbose_name="Initiative 1 URL"
    )

    initiative_title2 = models.CharField(
        max_length=255, blank=True, default="", verbose_name="Initiative 2 Title"
    )
    initiative_description2 = models.TextField(
        blank=True,
        default="",
        verbose_name="Initiative 2 Description (100 – 350 characters)",
    )
    initiative_url2 = models.URLField(
        max_length=255, blank=True, default="", verbose_name="Initiative 2 URL"
    )

    initiative_title3 = models.CharField(
        max_length=255, blank=True, default="", verbose_name="Initiative 3 Title"
    )
    initiative_description3 = models.TextField(
        blank=True,
        default="",
        verbose_name="Initiative 3 Description (100 – 350 characters)",
    )
    initiative_url3 = models.URLField(
        max_length=255, blank=True, default="", verbose_name="Initiative 3 URL"
    )

    objects = models.Manager()
    active = ActiveOrganizationManager()

    def __str__(self):
        return self.display_name

    def get_absolute_staff_url(self):
        return reverse("staff:organization-view", kwargs={"pk": self.id})

    def get_absolute_url(self):
        return reverse("crm:organization-view", kwargs={"pk": self.id})

    def get_logo_small_url(self):
        return u"https://www.oeconsortium.org/media/%s" % self.logo_small

    def save(self, force_insert=False, force_update=False, using=None):
        if not self.slug:
            slug = slugify(self.display_name)[:30]
            if Organization.objects.filter(slug=slug).exists():
                slug = slug[:29] + "2"
            self.slug = slug

        super(Organization, self).save(
            force_insert=force_insert, force_update=force_update, using=using
        )

    def get_membership_due_amount(self):
        # Sustaining members
        if self.membership_status in [7] or self.billing_type in [
            "custom",
            "consortia",
            "waiver",
        ]:
            return 0  # manually processed

        if self.associate_consortium == "CCCOER":
            return 650

        try:
            previous_invoice = self.billinglog_set.filter(
                log_type="create_invoice", invoice_year=settings.PREVIOUS_INVOICE_YEAR
            ).latest("id")
            return previous_invoice.amount
        except BillingLog.DoesNotExist:
            pass

        # (8 , 'Corporate Members - Basic'),
        if self.membership_type in [8]:
            return 1250

        return 900

    def get_invoice_status(self):
        return {
            "create_invoice": self.billinglog_set.filter(
                log_type="create_invoice", invoice_year=settings.DEFAULT_INVOICE_YEAR
            ).exists(),
            "send_invoice": self.billinglog_set.filter(
                log_type="send_invoice", invoice_year=settings.DEFAULT_INVOICE_YEAR
            ).exists(),
        }

    def get_last_year_invoice_status(self):
        return {
            "create_invoice": self.billinglog_set.filter(
                log_type="create_invoice", invoice_year=settings.PREVIOUS_INVOICE_YEAR
            ).exists(),
            "send_invoice": self.billinglog_set.filter(
                log_type="send_invoice", invoice_year=settings.PREVIOUS_INVOICE_YEAR
            ).exists(),
        }

    def get_consortia_members(self):
        consortia = None

        if self.slug == "cccoer":
            consortia = "CCCOER"
        elif self.slug == "japan-ocw-consortium":
            consortia = "JOCWC"
        elif self.slug == "korea-ocw-consortium":
            consortia = "KOCWC"
        elif self.slug == "taiwan-ocw-consortium":
            consortia = "TOCEC"
        elif self.slug == "turkish-ocw-consortium":
            consortia = "Turkish OCWC"
        elif self.slug == "taiwan-ocw-consortium":
            consortia = "TOCWC"
        elif self.slug == "universia":
            consortia = "UNIVERSIA"
        elif self.slug == "ocwfrance":
            consortia = "FOCW"

        if not consortia:
            return Organization.objects.none()

        return Organization.objects.filter(associate_consortium=consortia)

    def can_vote(self):
        if self.membership_status in (2, 5, 7):  # exclude grace (3) from voting
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
        text = text.replace("- MRC", "").replace("- DC", "").strip()
        return text

    def get_billing_address(self):
        try:
            address = self.address_set.filter(address_type="billing")[0]
        except IndexError:
            address = self.address_set.filter(address_type="primary")[0]

        return address

    def get_geo(self):
        try:
            address = self.address_set.filter(address_type="primary")[0]
            return {"latitude": address.latitude, "longitude": address.longitude}
        except IndexError:
            try:
                address = self.address_set.filter(address_type="billing")[0]
                return {"latitude": address.latitude, "longitude": address.longitude}
            except IndexError:
                pass

    def get_last_paid_invoice(self):
        return self.billinglog_set.filter(
            log_type__in=["create_paid_invoice", "create_payment"]
        ).latest("id")

    def get_lead_contact(self):
        return self.contact_set.filter(contact_type=6).latest("id")

    def sync_quickbooks_customer(self, qb_client):
        if settings.QB_ACTIVE and qb_client:
            if not self.qbo_id:
                customer = Customer()
            else:
                customer = Customer.get(self.qbo_id, qb=qb_client)

            customer.CompanyName = self.display_name
            customer.DisplayName = self.display_name
            customer.PrintOnCheckName = self.display_name

            billing_address = self.get_billing_address()
            if billing_address:
                customer.BillAddr = QuickBooksAddress()
                customer.BillAddr.Line1 = billing_address.street_address
                customer.BillAddr.Line2 = billing_address.supplemental_address_1
                customer.BillAddr.Line3 = billing_address.supplemental_address_2

                customer.BillAddr.City = billing_address.city
                customer.BillAddr.Country = billing_address.country.name
                customer.BillAddr.CountrySubDivisionCode = (
                    billing_address.state_province_abbr
                )
                customer.BillAddr.PostalCode = "{} {}".format(
                    billing_address.postal_code, billing_address.postal_code_suffix
                ).strip()

            primary_contact = self.contact_set.filter(contact_type=6)[0]
            accounting_contacts = self.contact_set.filter(contact_type=13)
            if accounting_contacts:
                accounting_emails = [
                    accounting_contact.email
                    for accounting_contact in accounting_contacts
                ]
            else:
                accounting_emails = [primary_contact.email]

            customer.PrimaryEmailAddr = EmailAddress()
            customer.PrimaryEmailAddr.Address = ", ".join(accounting_emails)

            customer.GivenName = primary_contact.first_name
            customer.FamilyName = primary_contact.last_name

            customer.save(qb=qb_client)

            self.qbo_id = customer.Id
            self.save()


# CONTACT_TYPE_CHOICES = (
#   ('lead', 'Main contact'),
#   ('tech', 'Technical contact'),
#   ('billing', 'Billing contact')
# )

CONTACT_TYPE_CHOICES = (
    (4, "Employee of"),
    (6, "Lead Contact for"),
    (9, "Certifier for"),
    (10, "Voting Representative"),
    (11, "Affiliated with"),
    (12, "AC Member of"),
    (13, "Accounting Contact"),
)


class Contact(models.Model):
    organization = models.ForeignKey(Organization, models.CASCADE)

    contact_type = models.IntegerField(choices=CONTACT_TYPE_CHOICES)
    email = models.EmailField(max_length=255)

    first_name = models.CharField(max_length=255, blank=True, default="")
    last_name = models.CharField(max_length=255, blank=True, default="")
    job_title = models.CharField(max_length=255, blank=True, default="")

    bouncing = models.BooleanField(default=False)

    def __str__(self):
        return self.email


ADDRESS_TYPE = (("primary", "Primary Address"), ("billing", "Billing Address"))


class Address(models.Model):
    organization = models.ForeignKey(Organization, models.CASCADE)
    address_type = models.CharField(
        max_length=25, choices=ADDRESS_TYPE, default="primary"
    )

    street_address = models.CharField(
        max_length=255, blank=True, help_text="Street address with street number"
    )
    supplemental_address_1 = models.CharField(max_length=255, blank=True)
    supplemental_address_2 = models.CharField(max_length=255, blank=True)

    city = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=50, blank=True)
    postal_code_suffix = models.CharField(max_length=255, blank=True)

    state_province = models.CharField(max_length=255, blank=True)
    state_province_abbr = models.CharField(max_length=255, blank=True)

    country = models.ForeignKey(
        Country, models.CASCADE, blank=True, null=True, verbose_name="Country/region"
    )

    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        if self.country:
            return u"%s %s %s" % (self.country.name, self.city, self.street_address)
        else:
            return u"%s %s" % (self.city, self.street_address)

    def full_postal_address(self):
        if self.country:
            address = [self.street_address]
            if self.supplemental_address_1:
                address.append(self.supplemental_address_1)
            if self.supplemental_address_2:
                address.append(self.supplemental_address_2)

            address.append(
                u"{} {} {}".format(self.postal_code, self.postal_code_suffix, self.city)
            )
            address.append(u"{} {}".format(self.state_province, self.country.name))

            address = u"\n".join(address).replace(", ,", ", ")
            return address

        return ""

    def save(self, force_insert=False, force_update=False, using=None):
        if self.country:
            g = geocoders.Nominatim(user_agent="OEG-CRM")

            address_string = u"{}, {} {} {}, {}, {}".format(
                self.street_address,
                self.postal_code,
                self.postal_code_suffix,
                self.city,
                self.state_province,
                self.country.name.replace(", Republic of", ""),
            )
            address_string = address_string.replace(", ,", ", ")

            try:
                place, (lat, lng) = g.geocode(address_string)

                if lat:
                    self.latitude = lat
                    self.longitude = lng
            except TypeError:
                pass

        super(Address, self).save(
            force_insert=force_insert, force_update=force_update, using=using
        )

    def get_absolute_url(self):
        return self.organization.get_absolute_url()


APPLICATION_MEMBERSHIP_TYPE = ()

APPLICATION_STATUS_CHOICES = (
    ("Submitted", "Submitted"),
    ("Committee", "Sent to Committee"),
    ("Approved", "Approved"),
    ("Rejected", "Rejected"),
    ("Spam", "Spam"),
    ("RequestedMoreInfo", "Requested more information"),
)

ORGANIZATION_TYPE_CHOICES = (
    ("university", "University"),
    ("npo", "Non-Profit Organization"),
    ("ngo", "Non-Governmental Organization"),
    ("regionalconsortium", "Regional Consortium"),
    ("software", "Software Development"),
    ("commercial", "Commercial Entity"),
)

SIMPLIFIED_MEMBERSHIP_TYPE_CHOICES = (
    ("institutional", "Institutional Member"),
    ("associate", "Associate Consortium Member"),
    ("organizational", "Organizational Member"),
    ("corporate", "Corporate Member"),
)

CORPORATE_SUPPORT_CHOICES = (
    ("basic", "Basic - $1,000 annual membership fee"),
    # ('premium', 'Premium - $5,000 annual membership fee'),
    ("sustaining", "Sustaining - $30,000 contribution annual membership fee"),
    ("bronze", "Bronze - $60,000 contribution annual membership fee"),
    ("silver", "Silver - $100,000 contribution annual membership fee"),
    ("gold", "Gold - $150,000 contribution annual membership fee"),
    ("platinum", "Platinum - $250,000 contribution annual membership fee"),
)

IS_ACCREDITED_CHOICES = ((1, "Yes"), (0, "No"))


class MembershipApplication(models.Model):
    organization = models.ForeignKey(
        Organization,
        models.CASCADE,
        blank=True,
        null=True,
        help_text="Should be empty, unless application is approved",
    )
    membership_type = models.IntegerField(
        choices=ORGANIZATION_MEMBERSHIP_TYPE_CHOICES,
        blank=True,
        null=True,
        default=None,
    )

    display_name = models.CharField(
        max_length=255, blank=True, verbose_name="Institution Name"
    )

    edit_link_key = models.CharField(max_length=255, blank=True)
    view_link_key = models.CharField(max_length=255, blank=True)

    description = models.TextField(
        blank=True,
        help_text="This information will be publicly displayed on your OEG profile site.",
    )

    legacy_application_id = models.IntegerField(blank=True, null=True)
    legacy_entity_id = models.IntegerField(blank=True, null=True)

    main_website = models.CharField(
        max_length=765, blank=True, verbose_name=u"Institution Website URL"
    )
    ocw_website = models.CharField(
        max_length=765,
        blank=True,
        verbose_name=u"Open Educational Resources (OER) or OpenCourseWare (OCW) Website",
    )

    logo_large = models.ImageField(
        max_length=765,
        blank=True,
        upload_to="logos",
        verbose_name=u"Submit an institution logo. Must be at least 500x500 pixels in a PNG, PDF, EPS, or JPG format.",
    )
    logo_small = models.CharField(max_length=765, blank=True)

    institution_country = models.ForeignKey(
        Country, models.CASCADE, blank=True, null=True
    )

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

    organization_type = models.CharField(
        max_length=765, blank=True, choices=ORGANIZATION_TYPE_CHOICES, default=""
    )
    institution_type = models.CharField(
        max_length=25,
        blank=True,
        choices=INSTITUTION_TYPE_CHOICES,
        default="",
        verbose_name="Institution Category",
    )

    is_accredited = models.NullBooleanField(
        default=None, choices=IS_ACCREDITED_CHOICES, blank=True
    )
    accreditation_body = models.CharField(max_length=765, blank=True, default="")
    ocw_launch_date = models.DateTimeField(null=True, blank=True)

    support_commitment = models.TextField(blank=True)

    app_status = models.CharField(
        choices=APPLICATION_STATUS_CHOICES, max_length=255, blank=True
    )
    created = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    modified = models.DateTimeField(blank=True)  # , null=True, auto_now=True)

    # address
    street_address = models.CharField(
        max_length=255, blank=True, help_text="Street address with a street number"
    )
    supplemental_address_1 = models.CharField(
        max_length=255, blank=True, verbose_name=u"Street Address 2"
    )
    supplemental_address_2 = models.CharField(
        max_length=255, blank=True, verbose_name=u"Street Address 3"
    )

    city = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=50, blank=True)

    state_province = models.CharField(
        max_length=255, blank=True, verbose_name=u"State/Province"
    )
    country = models.ForeignKey(
        Country, models.CASCADE, blank=True, null=True, related_name="app_country"
    )

    email = models.EmailField(max_length=255, blank=True)

    first_name = models.CharField(max_length=255, blank=True, default="")
    last_name = models.CharField(max_length=255, blank=True, default="")
    job_title = models.CharField(max_length=255, blank=True, default="")

    simplified_membership_type = models.CharField(
        max_length=255, blank=True, choices=SIMPLIFIED_MEMBERSHIP_TYPE_CHOICES
    )
    corporate_support_levels = models.CharField(
        max_length=255, blank=True, choices=CORPORATE_SUPPORT_CHOICES
    )
    associate_consortium = models.CharField(
        max_length=255,
        choices=ORGANIZATION_ASSOCIATED_CONSORTIUM,
        blank=True,
        default="",
    )

    moa_terms = models.NullBooleanField(null=True)
    terms_of_use = models.NullBooleanField(null=True)
    coppa = models.NullBooleanField(null=True)

    initiative_title1 = models.CharField(
        max_length=255, blank=True, default="", verbose_name="Title"
    )
    initiative_description1 = models.TextField(
        blank=True, default="", verbose_name="Description (100 – 350 characters)"
    )
    initiative_url1 = models.URLField(
        max_length=255, blank=True, default="", verbose_name="URL"
    )

    initiative_title2 = models.CharField(
        max_length=255, blank=True, default="", verbose_name="Title"
    )
    initiative_description2 = models.TextField(
        blank=True, default="", verbose_name="Description (100 – 350 characters)"
    )
    initiative_url2 = models.URLField(
        max_length=255, blank=True, default="", verbose_name="URL"
    )

    initiative_title3 = models.CharField(
        max_length=255, blank=True, default="", verbose_name="Title"
    )
    initiative_description3 = models.TextField(
        blank=True, default="", verbose_name="Description (100 – 350 characters)"
    )
    initiative_url3 = models.URLField(
        max_length=255, blank=True, default="", verbose_name="URL"
    )

    def save(self, force_insert=False, force_update=False, using=None):
        if not self.legacy_application_id:
            if not self.edit_link_key:
                self.edit_link_key = uuid.uuid4().hex

        if not self.view_link_key:
            self.view_link_key = uuid.uuid4().hex

        if not self.modified:
            self.modified = datetime.datetime.now()
        if not self.created:
            self.created = datetime.datetime.now()

        if self.first_name == self.last_name:
            self.app_status = "Spam"

        if "<a href" in self.description:
            self.app_status = "Spam"

        if not self.app_status:
            self.app_status = "Submitted"

        if self.app_status == "Approved" and not self.organization:
            self.organization = self._create_member()

        if not self.pk and not self.app_status == "Spam":
            self._send_notification_email()

        super(MembershipApplication, self).save(
            force_insert=force_insert, force_update=force_update, using=using
        )

    def get_absolute_url(self):
        # return reverse('crm:application-view', kwargs={'view_link_key':self.view_link_key})
        return "/application/view/%s/" % self.view_link_key

    def __str__(self):
        return "Application #%s" % self.id

    def _create_member(self):
        org, is_created = Organization.objects.get_or_create(
            display_name=self.display_name,
            membership_type=self.membership_type,
            defaults={
                "membership_status": 5,  # pending
                "associate_consortium": self.associate_consortium,
                "main_website": self.main_website,
                "ocw_website": self.ocw_website,
                "description": self.description,
                "support_commitment": self.support_commitment,
                "institution_type": self.institution_type,
                "initiative_description1": self.initiative_description1,
                "initiative_title1": self.initiative_title1,
                "initiative_url1": self.initiative_url1,
                "initiative_title2": self.initiative_title2,
                "initiative_description2": self.initiative_description2,
                "initiative_url2": self.initiative_url2,
                "initiative_title3": self.initiative_title3,
                "initiative_description3": self.initiative_description3,
                "initiative_url3": self.initiative_url3,
            },
        )

        contact, is_created = Contact.objects.get_or_create(
            organization=org,
            contact_type=6,  # Lead contact
            email=self.email,
            defaults={"first_name": self.first_name, "last_name": self.last_name},
        )

        try:
            user, is_created = User.objects.get_or_create(
                username=org.slug[:29], email=contact.email
            )
        except IntegrityError:
            user, is_created = User.objects.get_or_create(
                username="{}-{}".format(
                    org.slug[:20], int(round(random.random() * 10, 0))
                ),
                email=contact.email,
                last_login=datetime.datetime.now(),
            )

        org.user = user
        org.save()

        address, is_created = Address.objects.get_or_create(
            organization=org,
            street_address=self.street_address,
            defaults={
                "supplemental_address_1": self.supplemental_address_1,
                "supplemental_address_2": self.supplemental_address_2,
                "city": self.city,
                "postal_code": self.postal_code,
                "state_province": self.state_province,
                "country": self.country,
            },
        )

        send_mail(
            "New OEG Member: {}".format(self.display_name),
            "View member profile: https://www.oeconsortium.org/members/view/{}/".format(
                org.id
            ),
            "tech@oeglobal.org",
            ["staff@oeconsortium.org"],
        )

        return org

    def _send_notification_email(self):
        send_mail(
            "New Membership Application: %s" % self.display_name,
            "View application: https://members.oeglobal.org%s"
            % self.get_absolute_url(),
            "tech@oeglobal.org",
            ["memberapplications@ocwconsortium.org"],
        )


COMMENTS_APP_STATUS_CHOICES = (
    ("Requested More Info", "Requested More Info"),
    ("Spam", "Spam"),
    ("Approved", "Approved"),
)


class MembershipApplicationComment(models.Model):
    application = models.ForeignKey(MembershipApplication, models.CASCADE)

    legacy_comment_id = models.IntegerField(blank=True)
    legacy_app_id = models.IntegerField(blank=True)

    comment = models.TextField(blank=True)
    sent_email = models.BooleanField(default=False)
    app_status = models.CharField(
        max_length=255, blank=True
    )  # , choices=COMMENTS_APP_STATUS_CHOICES, blank=True)

    created = models.DateTimeField()  # auto_now_add=True


class ReportedStatistic(models.Model):
    organization = models.ForeignKey(Organization, models.CASCADE)
    report_month = models.CharField(max_length=6)
    report_year = models.CharField(max_length=12)
    site_visits = models.IntegerField()
    orig_courses = models.IntegerField(verbose_name=u"Original Courses")
    trans_courses = models.IntegerField(verbose_name=u"Translated Courses")
    orig_course_lang = models.TextField(
        blank=True, verbose_name=u"Original Courses Language"
    )
    trans_course_lang = models.TextField(
        blank=True, null=True, verbose_name=u"Translated Courses Language"
    )

    oer_resources = models.IntegerField(
        null=True, blank=True, verbose_name=u"Number of OER Resources"
    )
    trans_oer_resources = models.IntegerField(
        null=True, blank=True, verbose_name=u"Number of Translated OER Resources"
    )
    comment = models.TextField(blank=True, null=True, verbose_name=u"Comment")

    report_date = models.DateField(verbose_name=u"Reported period")
    last_modified = models.DateTimeField(auto_now_add=True)
    carry_forward = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse(
            "crm:reported-statistics-view", kwargs={"pk": self.organization.id}
        )


class LoginKey(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    email = models.EmailField()
    key = models.CharField(max_length=32)

    used = models.BooleanField(default=False)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s - %s" % (self.user, self.email)

    def save(self, force_insert=False, force_update=False, using=None):
        if not self.key:
            self.key = uuid.uuid4().hex

        super(LoginKey, self).save(
            force_insert=force_insert, force_update=force_update, using=using
        )

    def send_email(self):
        body = render_to_string(
            "mail-login/mail_body.txt", {"url": self.get_absolute_url()}
        )
        send_mail(
            "OEG Member portal login information",
            body,
            "memberservices@oeglobal.org",
            [self.email],
        )

    def get_absolute_url(self):
        return "/login/%s/" % self.key


BILLING_LOG_TYPE_CHOICES = (
    ("create_invoice", "Invoice"),
    ("send_invoice", "Send invoice via email"),
    ("create_paid_invoice", "Create paid invoice"),
    ("send_paid_invoice", "Send paid invoice via email"),
    ("create_note", "Accounting note"),
    ("create_general_note", "General note"),
    ("create_payment", "Payment"),
)


class BillingLog(models.Model):
    log_type = models.CharField(max_length=30, choices=BILLING_LOG_TYPE_CHOICES)
    organization = models.ForeignKey(Organization, models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, models.CASCADE)
    created_date = models.DateField(
        null=True, verbose_name="Created Date (year-month-day)"
    )

    amount = models.IntegerField(null=True)
    email = models.CharField(max_length=120, blank=True, verbose_name="Recepient email")
    invoice = models.ForeignKey("Invoice", models.CASCADE, null=True, blank=True)
    invoice_year = models.CharField(
        default=settings.DEFAULT_INVOICE_YEAR, max_length=10
    )
    invoice_number = models.CharField(max_length=60, null=True, blank=True)
    description = models.TextField(blank=True, default="")
    note = models.TextField(blank=True)

    email_subject = models.CharField(max_length=140, blank=True, verbose_name="Subject")
    email_body = models.TextField(blank=True, verbose_name="Message")

    qbo_id = models.IntegerField(null=True, blank=True, default=None)

    class Meta:
        ordering = ["-pub_date"]

    @staticmethod
    def _open_file(path_to_file, attempts=0, timeout=5, sleep_int=5):
        if (
            attempts < timeout
            and os.path.exists(path_to_file)
            and os.path.isfile(path_to_file)
        ):
            f = open(path_to_file, "rb")
            return f
        else:
            time.sleep(sleep_int)
            return BillingLog._open_file(path_to_file, attempts + 1)

    def send_email(self):
        message = EmailMessage(
            subject=self.email_subject,
            body=self.email_body,
            from_email="memberservices@oeglobal.org",
            to=[s.strip() for s in self.email.split(",")],
            bcc=[self.user.email],
        )
        pdf_path = os.path.join(settings.INVOICES_ROOT, self.invoice.pdf_filename)

        f = BillingLog._open_file(pdf_path)
        content = f.read()
        f.close()

        message.attach(
            filename="oec-invoice-%s.pdf" % self.invoice.invoice_number,
            content=content,
            mimetype="application/pdf",
        )
        message.send()

    def get_qbo_url(self):
        if not self.qbo_id:
            return None

        if self.log_type == "create_invoice":
            return "https://c1.qbo.intuit.com/app/invoice?txnId={}".format(self.qbo_id)

        if self.log_type == "create_payment":
            return "https://c1.qbo.intuit.com/app/recvpayment?txnId={}".format(
                self.qbo_id
            )


INVOICE_TYPE_CHOICES = (
    ("issued", "Normal issued invoice"),
    ("paid", "Invoice with paid watermark"),
)


class Invoice(models.Model):
    invoice_type = models.CharField(
        max_length=30, default="issued", choices=INVOICE_TYPE_CHOICES
    )
    organization = models.ForeignKey(Organization, models.CASCADE)
    invoice_number = models.CharField(max_length=30, blank=True)
    invoice_year = models.CharField(
        default=settings.DEFAULT_INVOICE_YEAR, max_length=10
    )
    amount = models.IntegerField()
    description = models.TextField(blank=True)

    pdf_filename = models.CharField(max_length=100, blank=True)
    access_key = models.CharField(max_length=32, blank=True)

    created_date = models.DateField(
        null=True, verbose_name="Created Date (year-month-day)"
    )

    paypal_link = models.TextField(blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Invoice %s (%s)" % (self.invoice_number, self.organization.display_name)

    def get_absolute_url(self):
        return reverse("staff:invoice-view", kwargs={"pk": self.id})

    def get_access_key_url(self):
        return reverse(
            "staff:invoice-phantomjs-view", kwargs={"access_key": self.access_key}
        )

    def get_pdf_url(self):
        return "%s%s" % (settings.INVOICES_URL, self.pdf_filename)

    def save(self, *args, **kwargs):
        if not self.access_key:
            self.access_key = uuid.uuid4().hex
        if not self.paypal_link:
            self.paypal_link = self._get_paypal_link()

        super(Invoice, self).save(*args, **kwargs)

    def generate_pdf(self):
        url = "%s%s" % (settings.INVOICES_PHANTOM_JS_HOST, self.get_access_key_url())
        filename = "invoice_%s_%s.pdf" % (self.pk, uuid.uuid4().hex)
        pdf_path = os.path.join(settings.INVOICES_ROOT, filename)

        print("print pdf start")
        print_pdf(url, pdf_path)
        print("print pdf end")

        self.pdf_filename = filename
        self.save()

    def _get_paypal_link(self):
        if self.amount == 225:
            return "https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=SSS6C5TBMRDJ2"
        if self.amount == 375:
            return "https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=Y6DLXHCB5E8JL"
        if self.amount == 525:
            return "https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=HJB7HSG28DC82"
        if self.amount == 750:
            return "https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=7LXJWSNC3DPMC"
        if self.amount == 1000:
            return "https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=Z8THX5FXTWCFS"

        return ""

    def create_qb_invoice(self, qb_client):
        invoice = QuickBooksInvoice()
        line = SalesItemLine()
        line.LineNum = 1
        line.Description = self.description
        line.Amount = self.amount
        # line.ServiceDate = qb_date_format(datetime.date(2019, 1, 1))
        line.SalesItemLineDetail = SalesItemLineDetail()
        line.SalesItemLineDetail.Qty = 1
        line.SalesItemLineDetail.UnitPrice = self.amount
        item = Item.choose(["MF"], field="SKU", qb=qb_client)[0]

        line.SalesItemLineDetail.ItemRef = item.to_ref()
        invoice.Line.append(line)

        customer = Customer.get(self.organization.qbo_id, qb=qb_client)
        invoice.CustomerRef = customer.to_ref()

        # term = Term.choose(['Net 30'], field='Name', qb=qb_client)[0]
        # invoice.SalesTermRef = term

        # invoice.TotalAmt = self.amount
        invoice.save(qb=qb_client)

        print(invoice.Id)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    qb_access_token = models.TextField(blank=True, default="")
    qb_refresh_token = models.TextField(blank=True, default="")
    qb_valid = models.BooleanField(default=False)
    qb_token_expires = models.DateTimeField(null=True, default=None)
    qb_refresh_expires = models.DateTimeField(null=True, default=None)
    qb_realm_id = models.TextField(blank=True, default="")

    def __str__(self):
        return self.user.username

    def update_qb_session_manager(self, code, realm_id):
        session_manager = Oauth2SessionManager(
            client_id=settings.QB_CLIENT_ID,
            client_secret=settings.QB_CLIENT_SECRET,
            base_url=settings.QB_CALLBACK_URL,
        )
        session_manager.get_access_tokens(code)

        self.qb_access_token = session_manager.access_token
        self.qb_refresh_token = session_manager.refresh_token
        self.qb_valid = True
        self.qb_token_expires = arrow.now().shift(seconds=3600).datetime
        self.qb_refresh_expires = arrow.now().shift(seconds=8726400).datetime
        self.qb_realm_id = realm_id
        self.save()

        Profile.objects.all().exclude(pk=self.id).update(qb_valid=False)

    def refresh_qb_session_manager(self):
        session_manager = Oauth2SessionManager(
            client_id=settings.QB_CLIENT_ID,
            client_secret=settings.QB_CLIENT_SECRET,
            base_url=settings.QB_CALLBACK_URL,
            refresh_token=self.qb_refresh_token,
        )
        session_manager.refresh_access_tokens(return_result=True)

        self.qb_access_token = session_manager.access_token
        self.qb_refresh_token = session_manager.refresh_token
        self.qb_valid = True
        self.qb_token_expires = arrow.now().shift(seconds=3600).datetime
        self.save()

        Profile.objects.all().exclude(pk=self.id).update(qb_valid=False)

        return session_manager

    @staticmethod
    def get_qb_client():
        if not settings.QB_ACTIVE:
            return None, None

        try:
            profile = Profile.objects.filter(qb_valid=True)[0]
        except IndexError:
            return None, None

        if profile.qb_valid:
            session_manager = Oauth2SessionManager(
                client_id=settings.QB_CLIENT_ID,
                client_secret=settings.QB_CLIENT_SECRET,
                access_token=profile.qb_access_token,
            )

            if profile.qb_token_expires < datetime.datetime.now():
                session_manager = profile.refresh_qb_session_manager()

            if settings.QB_ENVIRONMENT == "production":
                sandbox = False
            else:
                sandbox = True

            client = QuickBooks(
                sandbox=sandbox,
                session_manager=session_manager,
                company_id=profile.qb_realm_id,
                minorversion=36,
            )

            return client, profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created or not hasattr(instance, "profile"):
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
