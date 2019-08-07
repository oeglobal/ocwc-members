# -*- coding: utf-8 -*-
import datetime
from dateutil.relativedelta import relativedelta

from django import forms
from django.utils.safestring import mark_safe

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div, HTML

from .models import (
    MembershipApplication,
    ORGANIZATION_ASSOCIATED_CONSORTIUM,
    Organization,
    Address,
    BillingLog,
    BILLING_LOG_TYPE_CHOICES,
    ReportedStatistic,
)

SIMPLIFIED_MEMBERSHIP_TYPE_CHOICES = (
    (
        "institutional",
        mark_safe(
            'Institutional Member <i class="icon-question-sign" data-help-text="institutional"></i>'
        ),
    ),
    (
        "associate",
        mark_safe('Associate Consortium Member <i class="icon-question-sign"></i>'),
    ),
    (
        "organizational",
        mark_safe('Organizational Member <i class="icon-question-sign"></i>'),
    ),
    ("corporate", mark_safe('Corporate Member <i class="icon-question-sign"></i>')),
)

ORGANIZATION_ASSOCIATED_CONSORTIUM_CHOICES = filter(
    lambda x: x[0] not in ["CORE", "KOCWC"], ORGANIZATION_ASSOCIATED_CONSORTIUM
)


class MembershipApplicationModelForm(forms.ModelForm):
    associate_consortium = forms.ChoiceField(
        choices=(("", "---------"),)
        + tuple(ORGANIZATION_ASSOCIATED_CONSORTIUM_CHOICES),
        required=False,
    )

    moa_terms = forms.BooleanField(required=True, label="I agree to these terms")

    terms_of_use = forms.BooleanField(
        required=True, label="I agree to the terms of use for this website."
    )
    coppa = forms.BooleanField(
        required=True, label="I signify that I am 13 years of age or older."
    )

    main_website = forms.URLField(
        required=True, label="Main Website address (with http:// or https:// in front)"
    )

    initiative_url1 = forms.URLField(required=False, label="URL")
    initiative_url2 = forms.URLField(required=False, label="URL")
    initiative_url3 = forms.URLField(required=False, label="URL")
    captcha = ReCaptchaField()

    def __init__(self, *args, **kwargs):
        super(MembershipApplicationModelForm, self).__init__(*args, **kwargs)

        self.fields[
            "description"
        ].label = "Institution Description (500 - 1200 characters)"
        self.fields["support_commitment"].label = ""
        self.fields[
            "accreditation_body"
        ].help_text = "If your organization is accredited, please provide the name of the accreditation body here."
        self.fields["country"].help_text = mark_safe(
            "Select the country in which the institution is located. This will be used for grouping in the members display area on the website."
        )

        self.helper = FormHelper(self)
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                HTML(
                    '<div class="large-8 columns"><h3>Lead Contact Information</h3><p>(Person filling out the application who will also act as the lead contact for communications with the OEC)</p></div>'
                ),
                Div(
                    Div(
                        Field("first_name", required=True),
                        css_class="large-6 columns field-collapse text-full-width",
                    ),
                    Div(
                        Field("last_name", required=True),
                        css_class="large-6 columns field-collapse text-full-width",
                    ),
                    css_class="row",
                ),
                Field("job_title", required=True),
                Field("email", required=True),
                css_class="row",
            ),
            Div(
                HTML('<div class="large-8 columns"><h3>Member Profile</h3></div>'),
                Field("display_name", required=True),
                Field("description", required=True),
                Field("logo_large"),
                # Field('is_accredited', required=True),
                # 'accreditation_body',
                Field("main_website", required=True, placeholder="http://"),
                Field("institution_type", required=True),
                Field("associate_consortium"),
                # 'country',
                css_class="row",
            ),
            Div(
                HTML('<div class="large-8 columns"><h3>Address</h3></div>'),
                Field("street_address", required=True),
                "supplemental_address_1",
                "supplemental_address_2",
                Div(
                    Div(
                        Field("city", required=True),
                        css_class="large-6 columns field-collapse text-full-width",
                    ),
                    Div(
                        Field("postal_code", required=True),
                        css_class="large-6 columns field-collapse",
                    ),
                    css_class="row",
                ),
                "state_province",
                Field("country", required=True),
                css_class="row",
            ),
            Div(
                HTML('<div class="large-8 columns"><h3>Support Commitment</h3></div>'),
                HTML(
                    '<div class="large-8 columns"><p>Describe your motivation for joining OEC. Please include the '
                    "ways your organization supports or is planning to support the Open Education movement. "
                    "(1000 - 1500 characters)</p></div>"
                ),
                Field("support_commitment", required=True),
                css_class="row",
            ),
            Div(
                HTML('<div class="large-8 columns"><h3>Open Initiatives</h3></div>'),
                HTML(
                    '<div class="large-8 columns"><p>If you have several open initiatives with independent website '
                    "links please include them below with a brief description of each. (ex. OER repository, "
                    "Open MOOCs, Institutional Open Research, Open Textbooks, etc.)</p></div>"
                ),
                HTML(
                    '<div class="large-8 columns"><p>If you would like to share more than three open websites please '
                    "contact us at "
                    '<a href="mailto:memberservices@oeconsortium.org">memberservices@oeconsortium.org</a> '
                    "and we'll be happy to accommodate your needs.</div>"
                ),
                HTML('<div class="large-8 columns"><h4>Open initiative 1</h4></div>'),
                Field("initiative_title1"),
                Field("initiative_description1"),
                Field("initiative_url1"),
                HTML('<div class="large-8 columns"><h4>Open initiative 2</h4></div>'),
                Field("initiative_title2"),
                Field("initiative_description2"),
                Field("initiative_url2"),
                HTML('<div class="large-8 columns"><h4>Open initiative 3</h4></div>'),
                Field("initiative_title3"),
                Field("initiative_description3"),
                Field("initiative_url3"),
                css_class="row",
            ),
            Div(
                HTML(
                    '<div class="large-8 columns"><h3>Memorandum of Association</h3></div>'
                ),
                HTML('<div class="moa-text large-8 columns"></div>'),
                Field("moa_terms", required=True),
                HTML(
                    '<div class="large-8 columns"><h3>Website Terms and Conditions</h3></div>'
                ),
                HTML('<div class="terms-text large-8 columns"></div>'),
                Field("terms_of_use", required=True),
                HTML(
                    '<div class="large-8 columns"><h3>Children\'s Online '
                    "Privacy Protection Act Compliance</h3></div>"
                ),
                HTML('<div class="coppa-text large-8 columns"></div>'),
                Field("coppa", required=True),
                Field("captcha", required=True),
                css_class="row",
            ),
        )
        self.helper.layout.append(Submit("save", "save"))

    def clean(self):
        cleaned_data = super(MembershipApplicationModelForm, self).clean()
        return cleaned_data

    class Meta:
        model = MembershipApplication
        exclude = ("id",)


class MemberLoginForm(forms.Form):
    organization = forms.ChoiceField()
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(MemberLoginForm, self).__init__(*args, **kwargs)
        self.fields["organization"].choices = [
            (x.id, x.display_name) for x in Organization.active.all()
        ]

    def clean(self):
        cleaned_data = super(MemberLoginForm, self).clean()

        email = cleaned_data.get("email", "").strip()
        org = cleaned_data.get("organization")

        if (
            org
            and email
            and not Organization.active.filter(pk=org, contact__email__iexact=email)
        ):
            raise forms.ValidationError(
                "E-mail you entered is not associated with selected organization."
                + "Please contact members services if you require assistance.",
                code="invalid-email",
            )

        return cleaned_data


class AddressModelForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = (
            "street_address",
            "supplemental_address_1",
            "supplemental_address_2",
            "city",
            "postal_code",
            "state_province",
            "country",
            "address_type",
        )


class BillingLogForm(forms.ModelForm):
    log_type = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=(
            ("create_general_note", "Add a General note"),
            ("create_note", "Add an Accounting note"),
        ),
        label="Action",
    )

    def __init__(self, *args, **kwargs):
        super(BillingLogForm, self).__init__(*args, **kwargs)

        self.fields["organization"].widget = forms.HiddenInput()
        self.fields["user"].widget = forms.HiddenInput()

        self.helper = FormHelper(self)

        self.helper.layout = Layout(
            Div(Field("log_type", ng_model="logtype"), css_class="row"),
            Div(
                HTML("<p>Note will be visible to other staff members</p>"),
                Field("note"),
                ng_show="logtype === 'create_note' || logtype === 'create_general_note",
            ),
            Field("organization"),
            Field("user"),
            Submit("submit", "submit"),
        )

    class Meta:
        model = BillingLog
        fields = ("log_type", "organization", "user", "note")


class ReportedStatisticModelForm(forms.ModelForm):
    report_date = forms.ChoiceField(label="Reported period, until:")

    def __init__(self, *args, **kwargs):
        self.obj = kwargs.get("instance", None)
        if self.obj:
            self.organization = self.obj.organization
        else:
            self.organization = kwargs.pop("organization")

        super(ReportedStatisticModelForm, self).__init__(*args, **kwargs)

        base = datetime.datetime(2016, 3, 1, 0, 0, 0)
        self.fields["report_date"].choices = [
            (i.strftime("%Y-%m-%d"), i.strftime("%B %Y"))
            for i in [base - relativedelta(months=x * 3) for x in range(0, 20)]
        ]
        if not self.obj:
            try:
                previous_statistic = ReportedStatistic.objects.filter(
                    organization=self.organization
                ).latest("report_date")
            except ReportedStatistic.DoesNotExist:
                previous_statistic = None

            if previous_statistic:
                for item in [
                    "site_visits",
                    "orig_courses",
                    "trans_courses",
                    "orig_course_lang",
                    "trans_course_lang",
                    "oer_resources",
                    "trans_oer_resources",
                ]:
                    self.fields[item].initial = getattr(previous_statistic, item)

    def clean(self):
        cleaned_data = super(ReportedStatisticModelForm, self).clean()

        if (
            not self.obj
            and ReportedStatistic.objects.filter(
                organization=self.organization, report_date=cleaned_data["report_date"]
            ).exists()
        ):
            raise forms.ValidationError(
                "Reported statistic for this interval already exists. Please edit previous entry."
            )

        return cleaned_data

    def save(self, commit=True):
        instance = super(ReportedStatisticModelForm, self).save(commit=False)
        instance.organization = self.organization

        if commit:
            instance.save()
        return instance

    class Meta:
        model = ReportedStatistic
        fields = (
            "site_visits",
            "orig_courses",
            "trans_courses",
            "orig_course_lang",
            "trans_course_lang",
            "oer_resources",
            "trans_oer_resources",
            "comment",
            "report_date",
        )
