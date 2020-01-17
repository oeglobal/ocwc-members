# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="Address",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "address_type",
                    models.CharField(
                        default=b"primary",
                        max_length=25,
                        choices=[
                            (b"primary", b"Primary Address"),
                            (b"billing", b"Billing Address"),
                        ],
                    ),
                ),
                (
                    "street_address",
                    models.CharField(
                        help_text=b"Street address with street number",
                        max_length=255,
                        blank=True,
                    ),
                ),
                (
                    "supplemental_address_1",
                    models.CharField(max_length=255, blank=True),
                ),
                (
                    "supplemental_address_2",
                    models.CharField(max_length=255, blank=True),
                ),
                ("city", models.CharField(max_length=255, blank=True)),
                ("postal_code", models.CharField(max_length=50, blank=True)),
                ("postal_code_suffix", models.CharField(max_length=255, blank=True)),
                ("state_province", models.CharField(max_length=255, blank=True)),
                ("state_province_abbr", models.CharField(max_length=255, blank=True)),
                ("latitude", models.FloatField(null=True, blank=True)),
                ("longitude", models.FloatField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="BillingLog",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "log_type",
                    models.CharField(
                        max_length=30,
                        choices=[
                            (b"create_invoice", b"Create new invoice"),
                            (b"send_invoice", b"Send invoice via email"),
                            (b"create_paid_invoice", b"Create paid invoice"),
                            (b"send_paid_invoice", b"Send paid invoice via email"),
                            (b"create_note", b"Add a note"),
                        ],
                    ),
                ),
                ("pub_date", models.DateTimeField(auto_now_add=True)),
                (
                    "created_date",
                    models.DateField(
                        null=True, verbose_name=b"Created Date (year-month-day)"
                    ),
                ),
                ("amount", models.IntegerField(null=True)),
                (
                    "email",
                    models.CharField(
                        max_length=120, verbose_name=b"Recepient email", blank=True
                    ),
                ),
                ("invoice_year", models.CharField(default=b"2017", max_length=10)),
                (
                    "invoice_number",
                    models.CharField(max_length=60, null=True, blank=True),
                ),
                ("description", models.TextField(default=b"", blank=True)),
                ("note", models.TextField(blank=True)),
                (
                    "email_subject",
                    models.CharField(
                        max_length=140, verbose_name=b"Subject", blank=True
                    ),
                ),
                ("email_body", models.TextField(verbose_name=b"Message", blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="Contact",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "contact_type",
                    models.IntegerField(
                        choices=[
                            (4, b"Employee of"),
                            (6, b"Lead Contact for"),
                            (9, b"Certifier for"),
                            (10, b"Voting Representative"),
                            (11, b"Affiliated with"),
                            (12, b"AC Member of"),
                        ]
                    ),
                ),
                ("email", models.EmailField(max_length=255)),
                (
                    "first_name",
                    models.CharField(default=b"", max_length=255, blank=True),
                ),
                (
                    "last_name",
                    models.CharField(default=b"", max_length=255, blank=True),
                ),
                (
                    "job_title",
                    models.CharField(default=b"", max_length=255, blank=True),
                ),
                ("bouncing", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Continent",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("name", models.CharField(unique=True, max_length=192, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="Country",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("name", models.CharField(unique=True, max_length=192, blank=True)),
                ("iso_code", models.CharField(unique=True, max_length=6, blank=True)),
                ("developing", models.BooleanField()),
                (
                    "continent",
                    models.ForeignKey(
                        on_delete=models.CASCADE,
                        blank=True,
                        to="crm.Continent",
                        null=True,
                    ),
                ),
            ],
            options={"ordering": ("name",)},
        ),
        migrations.CreateModel(
            name="Invoice",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "invoice_type",
                    models.CharField(
                        default=b"issued",
                        max_length=30,
                        choices=[
                            (b"issued", b"Normal issued invoice"),
                            (b"paid", b"Invoice with paid watermark"),
                        ],
                    ),
                ),
                ("invoice_number", models.CharField(max_length=30, blank=True)),
                ("invoice_year", models.CharField(default=b"2017", max_length=10)),
                ("amount", models.IntegerField()),
                ("description", models.TextField(blank=True)),
                ("pdf_filename", models.CharField(max_length=100, blank=True)),
                ("access_key", models.CharField(max_length=32, blank=True)),
                (
                    "created_date",
                    models.DateField(
                        null=True, verbose_name=b"Created Date (year-month-day)"
                    ),
                ),
                ("paypal_link", models.TextField(blank=True)),
                ("pub_date", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="LoginKey",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("email", models.EmailField(max_length=254)),
                ("key", models.CharField(max_length=32)),
                ("used", models.BooleanField(default=False)),
                ("pub_date", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MembershipApplication",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "membership_type",
                    models.IntegerField(
                        default=None,
                        max_length=10,
                        null=True,
                        blank=True,
                        choices=[
                            (5, b"Institutional Members"),
                            (10, b"Institutional Members - MRC"),
                            (11, b"Institutional Members - DC"),
                            (12, b"Institutional Members - DC - MRC"),
                            (9, b"Associate Institutional Members"),
                            (17, b"Associate Institutional Members - DC"),
                            (6, b"Organizational Members"),
                            (13, b"Organizational Members - DC"),
                            (18, b"Organizational Members - MRC"),
                            (7, b"Associate Consortium Members"),
                            (14, b"Associate Consortium Members - DC"),
                            (8, b"Corporate Members - Basic"),
                            (15, b"Corporate Members - Premium"),
                            (16, b"Corporate Members - Sustaining"),
                        ],
                    ),
                ),
                (
                    "display_name",
                    models.CharField(
                        max_length=255, verbose_name=b"Institution Name", blank=True
                    ),
                ),
                ("edit_link_key", models.CharField(max_length=255, blank=True)),
                ("view_link_key", models.CharField(max_length=255, blank=True)),
                (
                    "description",
                    models.TextField(
                        help_text=b"Please write between 1000 \xe2\x80\x93 1500 characters. <br />This information will be publicly displayed on your OEG profile site.",
                        blank=True,
                    ),
                ),
                ("legacy_application_id", models.IntegerField(null=True, blank=True)),
                ("legacy_entity_id", models.IntegerField(null=True, blank=True)),
                (
                    "main_website",
                    models.CharField(
                        max_length=765, verbose_name="Main Website address", blank=True
                    ),
                ),
                (
                    "ocw_website",
                    models.CharField(
                        max_length=765,
                        verbose_name="Open Educational Resources (OER) or OpenCourseWare (OCW) Website",
                        blank=True,
                    ),
                ),
                (
                    "logo_large",
                    models.ImageField(
                        upload_to=b"logos",
                        max_length=765,
                        verbose_name="Logo of your institution (at least 500x500px PNG or a vector (PDF, EPS) file)",
                        blank=True,
                    ),
                ),
                ("logo_small", models.CharField(max_length=765, blank=True)),
                ("rss_course_feed", models.CharField(max_length=765, blank=True)),
                ("rss_referral_link", models.CharField(max_length=765, blank=True)),
                (
                    "rss_course_feed_language",
                    models.CharField(max_length=765, blank=True),
                ),
                ("agreed_to_terms", models.CharField(max_length=765, blank=True)),
                ("agreed_criteria", models.CharField(max_length=765, blank=True)),
                ("contract_version", models.CharField(max_length=765, blank=True)),
                ("ocw_software_platform", models.CharField(max_length=765, blank=True)),
                ("ocw_platform_details", models.TextField(blank=True)),
                ("ocw_site_hosting", models.CharField(max_length=765, blank=True)),
                ("ocw_site_approved", models.NullBooleanField()),
                (
                    "ocw_published_languages",
                    models.CharField(max_length=765, blank=True),
                ),
                ("ocw_license", models.CharField(max_length=765, blank=True)),
                (
                    "organization_type",
                    models.CharField(
                        default=b"",
                        max_length=765,
                        blank=True,
                        choices=[
                            (b"university", b"Higher Education Institution"),
                            (b"npo", b"Non-Profit Organization"),
                            (b"ngo", b"Non-Governmental Organization"),
                            (b"regionalconsortium", b"Regional Consortium"),
                            (b"software", b"Software Development"),
                            (b"commercial", b"Commercial Entity"),
                        ],
                    ),
                ),
                (
                    "institution_type",
                    models.CharField(
                        default=b"",
                        max_length=25,
                        blank=True,
                        choices=[
                            (b"higher-ed", b"Higher Education Institution"),
                            (b"secondary-ed", b"Secondary Education Institution"),
                            (b"primary-ed", b"Primary Education Institution"),
                            (b"npo", b"Non-Profit Organization"),
                            (b"ngo", b"Non-Governmental Organization"),
                            (b"igo", b"Intergovernmental Organization (IGO)"),
                            (b"gov", b"Governmental Entity"),
                            (b"consortium", b"Regional Consortium"),
                            (b"software", b"Software Development"),
                            (b"commercial", b"Commercial Entity"),
                        ],
                    ),
                ),
                (
                    "is_accredited",
                    models.NullBooleanField(
                        default=None, choices=[(1, b"Yes"), (0, b"No")]
                    ),
                ),
                (
                    "accreditation_body",
                    models.CharField(default=b"", max_length=765, blank=True),
                ),
                ("ocw_launch_date", models.DateTimeField(null=True, blank=True)),
                ("support_commitment", models.TextField(blank=True)),
                (
                    "app_status",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        choices=[
                            (b"Submitted", b"Submitted"),
                            (b"Committee", b"Sent to Committee"),
                            (b"Approved", b"Approved"),
                            (b"Rejected", b"Rejected"),
                            (b"Spam", b"Spam"),
                            (b"RequestedMoreInfo", b"Requested more information"),
                        ],
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("modified", models.DateTimeField(blank=True)),
                (
                    "street_address",
                    models.CharField(
                        help_text=b"Street address with a street number",
                        max_length=255,
                        blank=True,
                    ),
                ),
                (
                    "supplemental_address_1",
                    models.CharField(
                        max_length=255, verbose_name="Street Address 2", blank=True
                    ),
                ),
                (
                    "supplemental_address_2",
                    models.CharField(
                        max_length=255, verbose_name="Street Address 3", blank=True
                    ),
                ),
                ("city", models.CharField(max_length=255, blank=True)),
                ("postal_code", models.CharField(max_length=50, blank=True)),
                (
                    "state_province",
                    models.CharField(
                        max_length=255, verbose_name="State/Province", blank=True
                    ),
                ),
                ("email", models.EmailField(max_length=255, blank=True)),
                (
                    "first_name",
                    models.CharField(default=b"", max_length=255, blank=True),
                ),
                (
                    "last_name",
                    models.CharField(default=b"", max_length=255, blank=True),
                ),
                (
                    "job_title",
                    models.CharField(default=b"", max_length=255, blank=True),
                ),
                (
                    "simplified_membership_type",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        choices=[
                            (b"institutional", b"Institutional Member"),
                            (b"associate", b"Associate Consortium Member"),
                            (b"organizational", b"Organizational Member"),
                            (b"corporate", b"Corporate Member"),
                        ],
                    ),
                ),
                (
                    "corporate_support_levels",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        choices=[
                            (b"basic", b"Basic - $1,000 annual membership fee"),
                            (
                                b"sustaining",
                                b"Sustaining - $30,000 contribution annual membership fee",
                            ),
                            (
                                b"bronze",
                                b"Bronze - $60,000 contribution annual membership fee",
                            ),
                            (
                                b"silver",
                                b"Silver - $100,000 contribution annual membership fee",
                            ),
                            (
                                b"gold",
                                b"Gold - $150,000 contribution annual membership fee",
                            ),
                            (
                                b"platinum",
                                b"Platinum - $250,000 contribution annual membership fee",
                            ),
                        ],
                    ),
                ),
                (
                    "associate_consortium",
                    models.CharField(
                        default=b"",
                        max_length=255,
                        blank=True,
                        choices=[
                            (
                                b"CCCOER",
                                b"Community College Consortium for Open Educational Resources (CCCOER)",
                            ),
                            (b"CORE", b"CORE"),
                            (b"JOCWC", b"Japan OCW Consortium"),
                            (b"KOCWC", b"Korea OCW Consortium"),
                            (b"TOCWC", b"Taiwan OCW Consortium"),
                            (b"Turkish OCWC", b"Turkish OpenCourseWare Consortium"),
                            (b"UNIVERSIA", b"UNIVERSIA"),
                            (b"FOCW", b"OCW France"),
                            (b"OTHER", b"OTHER"),
                        ],
                    ),
                ),
                ("moa_terms", models.NullBooleanField()),
                ("terms_of_use", models.NullBooleanField()),
                ("coppa", models.NullBooleanField()),
                (
                    "initiative_description1",
                    models.TextField(
                        default=b"",
                        verbose_name=b"Description (100 \xe2\x80\x93 350 characters)",
                        blank=True,
                    ),
                ),
                (
                    "initiative_url1",
                    models.URLField(
                        default=b"", max_length=255, verbose_name=b"URL", blank=True
                    ),
                ),
                (
                    "initiative_description2",
                    models.TextField(
                        default=b"",
                        verbose_name=b"Description (100 \xe2\x80\x93 350 characters)",
                        blank=True,
                    ),
                ),
                (
                    "initiative_url2",
                    models.URLField(
                        default=b"", max_length=255, verbose_name=b"URL", blank=True
                    ),
                ),
                (
                    "initiative_description3",
                    models.TextField(
                        default=b"",
                        verbose_name=b"Description (100 \xe2\x80\x93 350 characters)",
                        blank=True,
                    ),
                ),
                (
                    "initiative_url3",
                    models.URLField(
                        default=b"", max_length=255, verbose_name=b"URL", blank=True
                    ),
                ),
                (
                    "country",
                    models.ForeignKey(
                        on_delete=models.CASCADE,
                        related_name="app_country",
                        blank=True,
                        to="crm.Country",
                        null=True,
                    ),
                ),
                (
                    "institution_country",
                    models.ForeignKey(
                        on_delete=models.CASCADE,
                        blank=True,
                        to="crm.Country",
                        null=True,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MembershipApplicationComment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("legacy_comment_id", models.IntegerField(blank=True)),
                ("legacy_app_id", models.IntegerField(blank=True)),
                ("comment", models.TextField(blank=True)),
                ("sent_email", models.BooleanField(default=False)),
                ("app_status", models.CharField(max_length=255, blank=True)),
                ("created", models.DateTimeField()),
                (
                    "application",
                    models.ForeignKey(
                        on_delete=models.CASCADE, to="crm.MembershipApplication"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Organization",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("legal_name", models.CharField(max_length=255, blank=True)),
                (
                    "display_name",
                    models.CharField(
                        max_length=255, verbose_name=b"Name of the organization"
                    ),
                ),
                ("slug", models.CharField(default=b"", unique=True, max_length=30)),
                (
                    "membership_type",
                    models.IntegerField(
                        max_length=10,
                        choices=[
                            (5, b"Institutional Members"),
                            (10, b"Institutional Members - MRC"),
                            (11, b"Institutional Members - DC"),
                            (12, b"Institutional Members - DC - MRC"),
                            (9, b"Associate Institutional Members"),
                            (17, b"Associate Institutional Members - DC"),
                            (6, b"Organizational Members"),
                            (13, b"Organizational Members - DC"),
                            (18, b"Organizational Members - MRC"),
                            (7, b"Associate Consortium Members"),
                            (14, b"Associate Consortium Members - DC"),
                            (8, b"Corporate Members - Basic"),
                            (15, b"Corporate Members - Premium"),
                            (16, b"Corporate Members - Sustaining"),
                        ],
                    ),
                ),
                (
                    "membership_status",
                    models.IntegerField(
                        max_length=10,
                        choices=[
                            (1, b"Applied"),
                            (2, b"Current"),
                            (3, b"Grace"),
                            (4, b"Expired"),
                            (5, b"Pending"),
                            (6, b"Cancelled"),
                            (7, b"Sustaining"),
                            (99, b"Example"),
                        ],
                    ),
                ),
                (
                    "associate_consortium",
                    models.CharField(
                        default=b"",
                        max_length=255,
                        blank=True,
                        choices=[
                            (
                                b"CCCOER",
                                b"Community College Consortium for Open Educational Resources (CCCOER)",
                            ),
                            (b"CORE", b"CORE"),
                            (b"JOCWC", b"Japan OCW Consortium"),
                            (b"KOCWC", b"Korea OCW Consortium"),
                            (b"TOCWC", b"Taiwan OCW Consortium"),
                            (b"Turkish OCWC", b"Turkish OpenCourseWare Consortium"),
                            (b"UNIVERSIA", b"UNIVERSIA"),
                            (b"FOCW", b"OCW France"),
                            (b"OTHER", b"OTHER"),
                        ],
                    ),
                ),
                (
                    "crmid",
                    models.CharField(
                        help_text=b"Legacy identifier", max_length=255, blank=True
                    ),
                ),
                ("main_website", models.TextField(max_length=255, blank=True)),
                (
                    "ocw_website",
                    models.TextField(
                        max_length=255, verbose_name=b"OCW Website", blank=True
                    ),
                ),
                ("description", models.TextField(blank=True)),
                (
                    "logo_large",
                    models.ImageField(max_length=255, upload_to=b"logos", blank=True),
                ),
                (
                    "logo_small",
                    models.ImageField(max_length=255, upload_to=b"logos", blank=True),
                ),
                ("rss_course_feed", models.CharField(max_length=255, blank=True)),
                (
                    "accreditation_body",
                    models.CharField(default=b"", max_length=255, blank=True),
                ),
                ("support_commitment", models.TextField(default=b"", blank=True)),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "institution_type",
                    models.CharField(
                        default=b"",
                        max_length=25,
                        blank=True,
                        choices=[
                            (b"higher-ed", b"Higher Education Institution"),
                            (b"secondary-ed", b"Secondary Education Institution"),
                            (b"primary-ed", b"Primary Education Institution"),
                            (b"npo", b"Non-Profit Organization"),
                            (b"ngo", b"Non-Governmental Organization"),
                            (b"igo", b"Intergovernmental Organization (IGO)"),
                            (b"gov", b"Governmental Entity"),
                            (b"consortium", b"Regional Consortium"),
                            (b"software", b"Software Development"),
                            (b"commercial", b"Commercial Entity"),
                        ],
                    ),
                ),
                (
                    "initiative_description1",
                    models.TextField(
                        default=b"",
                        verbose_name=b"Description (100 \xe2\x80\x93 350 characters)",
                        blank=True,
                    ),
                ),
                (
                    "initiative_url1",
                    models.URLField(
                        default=b"", max_length=255, verbose_name=b"URL", blank=True
                    ),
                ),
                (
                    "initiative_description2",
                    models.TextField(
                        default=b"",
                        verbose_name=b"Description (100 \xe2\x80\x93 350 characters)",
                        blank=True,
                    ),
                ),
                (
                    "initiative_url2",
                    models.URLField(
                        default=b"", max_length=255, verbose_name=b"URL", blank=True
                    ),
                ),
                (
                    "initiative_description3",
                    models.TextField(
                        default=b"",
                        verbose_name=b"Description (100 \xe2\x80\x93 350 characters)",
                        blank=True,
                    ),
                ),
                (
                    "initiative_url3",
                    models.URLField(
                        default=b"", max_length=255, verbose_name=b"URL", blank=True
                    ),
                ),
                (
                    "ocw_contact",
                    models.ForeignKey(
                        on_delete=models.CASCADE,
                        related_name="ocw_contact_user",
                        verbose_name="Primary contact inside OCW",
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=models.CASCADE,
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ReportedStatistic",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("report_month", models.CharField(max_length=6)),
                ("report_year", models.CharField(max_length=12)),
                ("site_visits", models.IntegerField()),
                ("orig_courses", models.IntegerField(verbose_name="Original Courses")),
                (
                    "trans_courses",
                    models.IntegerField(verbose_name="Translated Courses"),
                ),
                (
                    "orig_course_lang",
                    models.TextField(
                        verbose_name="Original Courses Language", blank=True
                    ),
                ),
                (
                    "trans_course_lang",
                    models.TextField(
                        null=True,
                        verbose_name="Translated Courses Language",
                        blank=True,
                    ),
                ),
                (
                    "oer_resources",
                    models.IntegerField(
                        null=True, verbose_name="Number of OER Resources", blank=True
                    ),
                ),
                (
                    "trans_oer_resources",
                    models.IntegerField(
                        null=True,
                        verbose_name="Number of Translated OER Resources",
                        blank=True,
                    ),
                ),
                (
                    "comment",
                    models.TextField(null=True, verbose_name="Comment", blank=True),
                ),
                ("report_date", models.DateField(verbose_name="Reported period")),
                ("last_modified", models.DateTimeField(auto_now_add=True)),
                ("carry_forward", models.BooleanField(default=False)),
                (
                    "organization",
                    models.ForeignKey(on_delete=models.CASCADE, to="crm.Organization"),
                ),
            ],
        ),
        migrations.AddField(
            model_name="membershipapplication",
            name="organization",
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                blank=True,
                to="crm.Organization",
                help_text=b"Should be empty, unless application is approved",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="invoice",
            name="organization",
            field=models.ForeignKey(on_delete=models.CASCADE, to="crm.Organization"),
        ),
        migrations.AddField(
            model_name="contact",
            name="organization",
            field=models.ForeignKey(on_delete=models.CASCADE, to="crm.Organization"),
        ),
        migrations.AddField(
            model_name="billinglog",
            name="invoice",
            field=models.ForeignKey(
                on_delete=models.CASCADE, blank=True, to="crm.Invoice", null=True
            ),
        ),
        migrations.AddField(
            model_name="billinglog",
            name="organization",
            field=models.ForeignKey(on_delete=models.CASCADE, to="crm.Organization"),
        ),
        migrations.AddField(
            model_name="billinglog",
            name="user",
            field=models.ForeignKey(
                on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="address",
            name="country",
            field=models.ForeignKey(
                on_delete=models.CASCADE, blank=True, to="crm.Country", null=True
            ),
        ),
        migrations.AddField(
            model_name="address",
            name="organization",
            field=models.ForeignKey(on_delete=models.CASCADE, to="crm.Organization"),
        ),
    ]
