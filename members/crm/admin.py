from django.contrib import admin
from django.utils.html import format_html
from django import forms

from .models import (
    Organization,
    Contact,
    Address,
    MembershipApplication,
    Country,
    ReportedStatistic,
    Invoice,
    BillingLog,
    LoginKey,
    Continent,
    Profile,
)


class ContactInline(admin.TabularInline):
    model = Contact
    extra = 1


class AddressInline(admin.StackedInline):
    model = Address
    extra = 1


class OrganizationAdmin(admin.ModelAdmin):
    list_filter = (
        "membership_type",
        "membership_status",
        "ocw_contact",
        "institution_type",
    )
    list_display = ("display_name", "associate_consortium", "membership_status")
    search_fields = ("display_name",)
    inlines = [ContactInline, AddressInline]
    fieldsets = (
        (
            "General",
            {
                "fields": (
                    "display_name",
                    "membership_type",
                    "membership_status",
                    "billing_type",
                    "associate_consortium",
                    "ocw_contact",
                )
            },
        ),
        ("Websites", {"fields": ("main_website", "ocw_website")}),
        (
            "Initiatives",
            {
                "fields": (
                    "initiative_description1",
                    "initiative_url1",
                    "initiative_description2",
                    "initiative_url2",
                    "initiative_description3",
                    "initiative_url3",
                )
            },
        ),
        (
            "Additional",
            {
                "fields": (
                    "legal_name",
                    "user",
                    "slug",
                    "qbo_id",
                    "description",
                    "logo_large",
                    "logo_small",
                    "accreditation_body",
                    "support_commitment",
                )
            },
        ),
    )


class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "address_type",
        "organization",
        "street_address",
        "city",
        "country",
        "latitude",
        "longitude",
    )


class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "organization_link",
        "contact_type",
    )
    search_fields = ("email", "first_name", "last_name")

    def organization_link(self, obj):
        return format_html(
            '<a href="/admin/crm/organization/%s/">%s</a>'
            % (obj.organization.id, obj.organization)
        )

    organization_link.allow_tags = True


class MembershipApplicationForm(forms.ModelForm):
    class Meta:
        model = MembershipApplication
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(MembershipApplicationForm, self).__init__(*args, **kwargs)

    def clean_membership_type(self):
        app_status = self.cleaned_data.get("app_status")
        membership_type = self.cleaned_data.get("membership_type")

        if app_status == "Approved":
            if not membership_type:
                raise forms.ValidationError("Please set Membership Type")

        return membership_type


class MembershipApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "display_name",
        "organization",
        "membership_type",
        "legacy_application_id",
        "main_website",
    )
    list_filter = ("app_status",)
    search_fields = ("display_name", "description")
    raw_id_fields = ("organization",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "app_status",
                    "display_name",
                    "description",
                    "membership_type",
                    "organization",
                )
            },
        ),
        (
            "General",
            {
                "fields": (
                    "organization_type",
                    "main_website",
                    "ocw_website",
                    "institution_country",
                    "logo_large",
                    "rss_course_feed",
                    "is_accredited",
                    "accreditation_body",
                    "support_commitment",
                )
            },
        ),
        (
            "Initiatives",
            {
                "fields": (
                    "initiative_description1",
                    "initiative_url1",
                    "initiative_description2",
                    "initiative_url2",
                    "initiative_description3",
                    "initiative_url3",
                )
            },
        ),
        (
            "Membership",
            {
                "fields": (
                    "simplified_membership_type",
                    "corporate_support_levels",
                    "associate_consortium",
                )
            },
        ),
        (
            "Address and Contact",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "job_title",
                    "street_address",
                    "supplemental_address_1",
                    "supplemental_address_2",
                    "city",
                    "postal_code",
                    "state_province",
                    "country",
                )
            },
        ),
    )
    form = MembershipApplicationForm


class MembershipApplicationCommentAdmin(admin.ModelAdmin):
    list_display = (
        "application",
        "legacy_comment_id",
        "legacy_app_id",
        "comment",
        "app_status",
    )
    list_filter = ("app_status",)


class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "iso_code", "developing", "active_count")
    list_filter = ("developing",)

    def active_count(self, obj):
        return obj.address_set.filter(
            organization__membership_status__in=(2, 3, 5, 7, 99)
        ).count()


class ReportedStatisticAdmin(admin.ModelAdmin):
    list_display = (
        "organization",
        "last_modified",
        "site_visits",
        "orig_courses",
        "trans_courses",
        "orig_course_lang",
        "trans_course_lang",
        "oer_resources",
        "trans_oer_resources",
    )
    search_fields = ("organization__display_name",)
    # list_filter = ('report_year',)


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("invoice_number", "organization", "pub_date")


class BillingLogAdmin(admin.ModelAdmin):
    list_display = ("log_type", "organization", "pub_date")


class ProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(MembershipApplication, MembershipApplicationAdmin)
# admin.site.register(MembershipApplicationComment, MembershipApplicationCommentAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Continent)
admin.site.register(ReportedStatistic, ReportedStatisticAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(BillingLog, BillingLogAdmin)
admin.site.register(LoginKey)
admin.site.register(Profile, ProfileAdmin)
