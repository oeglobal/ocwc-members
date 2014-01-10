# -*- coding: utf-8 -*-
from pprint import pprint

from django import forms
from django.utils.safestring import mark_safe

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div, HTML

from .models import MembershipApplication, ORGANIZATION_ASSOCIATED_CONSORTIUM, CORPORATE_SUPPORT_CHOICES, IS_ACCREDITED_CHOICES, Organization

SIMPLIFIED_MEMBERSHIP_TYPE_CHOICES = (
    ('institutional', mark_safe('Institutional Member <i class="icon-question-sign" data-help-text="institutional"></i>')),
    ('associate', mark_safe('Associate Consortium Member <i class="icon-question-sign"></i>')),
    ('organizational', mark_safe('Organizational Member <i class="icon-question-sign"></i>')),
    ('corporate', mark_safe('Corporate Member <i class="icon-question-sign"></i>'))
)

ORGANIZATION_ASSOCIATED_CONSORTIUM_CHOICES = ORGANIZATION_ASSOCIATED_CONSORTIUM

class MembershipApplicationModelForm(forms.ModelForm):
    simplified_membership_type = forms.ChoiceField(widget=forms.RadioSelect,
                                                    choices=SIMPLIFIED_MEMBERSHIP_TYPE_CHOICES,
                                                    label='')
    corporate_support_levels = forms.ChoiceField(widget=forms.RadioSelect,
                                                    choices=CORPORATE_SUPPORT_CHOICES,
                                                    label='Please select financial support level',
                                                    required=False)
    associate_consortium = forms.ChoiceField(widget=forms.RadioSelect,
                                                choices=ORGANIZATION_ASSOCIATED_CONSORTIUM_CHOICES,
                                                required=False)

    is_accredited = forms.ChoiceField(widget=forms.RadioSelect,
                                        choices=IS_ACCREDITED_CHOICES,
                                        label='Accredited Institution of Higher Education?')

    moa_terms = forms.BooleanField(required=True, label='I agree to these terms')

    terms_of_use = forms.BooleanField(required=True, label='I agree to the terms of use for this website.')
    coppa = forms.BooleanField(required=True, label="I signify that I am 13 years of age or older.")

    def __init__(self, *args, **kwargs):
        super(MembershipApplicationModelForm, self).__init__(*args, **kwargs)

        self.fields['description'].label = "Describe your institution"
        self.fields['support_commitment'].label = ''
        self.fields['accreditation_body'].help_text = 'If your organization is accredited, please provide the name of the accreditation body here.'
        self.fields['support_commitment'].help_text = 'Please describe your motivation for joining the OCW Consortium, including the ways your organization supports or is planning to support the OCW movement.'
        self.fields['country'].help_text = mark_safe("Select the country in which the institution is located. This will be used for grouping in the members display area on the website.<br/> (D) indicates that the country is classified as a 'developing economy' according to the <a href='http://www.imf.org/external/pubs/ft/weo/2008/01/weodata/groups.htm' target='_blank'>World Economic Outlook.</a>")

        self.helper = FormHelper(self)
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                HTML('<div class="large-8 columns"><h3>Membership type</h3><p>Please select the type of membership for which you are applying and the appropriate memorandum of association will be displayed.</p></div>'),
                Div(Field('simplified_membership_type', required=True), css_class='large-7 columns'),
                HTML('<div class="large-5 columns help_container"></div>'),
            css_class="row"),
            Div(
                HTML('<div class="large-8 columns"><h3>Memorandum of Association</h3><div class="moa-wrapper"><p>- Please select the type of membership for which you are applying and the appropriate memorandum of association will be displayed.</p></div></div>'),
                Div(Field('corporate_support_levels'), css_class='corporate_support_levels'),
                Div(Field('associate_consortium'), css_class='organization_consortia'),
                Field('moa_terms', required=True),
            css_class="row"),
            Div(
                HTML('<div class="large-8 columns"><h3>Support Commitment</h3></div>'),
                Field('support_commitment', required=True),
            css_class="row"),
            Div(
                HTML('<div class="large-8 columns"><h3>Member Profile</h3></div>'),
                Field('display_name', required=True),
                Field('description', required=True),
                Field('organization_type', required=True),

                Field('is_accredited', required=True),
                'accreditation_body',
                Field('main_website', required=True, placeholder='http://'),
                'ocw_website',
                # 'country',
            css_class="row"),
            Div(
                HTML('<div class="large-8 columns"><h3>Address</h3></div>'),
                Field('street_address', required=True),
                'supplemental_address_1',
                'supplemental_address_2',
                Div(
                    Div(Field('city', required=True), css_class="large-6 columns field-collapse text-full-width"),
                    Div(Field('postal_code', required=True), css_class="large-6 columns field-collapse"),
                css_class="row"),
                'state_province',
                Field('country', required=True),
            css_class="row"),
            Div(
                HTML('<div class="large-8 columns"><h3>Lead Contact Information</h3></div>'),
                Div(
                    Div(Field('first_name', required=True), css_class="large-6 columns field-collapse text-full-width"),
                    Div(Field('last_name', required=True), css_class="large-6 columns field-collapse text-full-width"),
                css_class="row"),
                Field('job_title', required=True),
                Field('email', required=True),
            css_class="row"),
            Div(
                HTML('<div class="large-8 columns"><h3>Website Terms and Conditions</h3></div>'),
                HTML('<div class="terms-text large-8 columns"></div>'),
                Field('terms_of_use', required=True),
                HTML('''<div class="large-8 columns"><h3>Children's Online Privacy Protection Act Compliance</h3></div>'''),
                HTML('<div class="coppa-text large-8 columns"></div>'),
                Field('coppa', required=True),
            css_class="row"),
        )
        self.helper.layout.append(Submit('save', 'save'))

    def clean(self):
        cleaned_data = super(MembershipApplicationModelForm, self).clean()

        simplified_membership_type = cleaned_data.get('simplified_membership_type')
        corporate_support_levels = cleaned_data.get('corporate_support_levels')
        associate_consortium = cleaned_data.get('associate_consortium')

        # raise validation errors for connected fields
        if simplified_membership_type == 'corporate' and not corporate_support_levels:
            self._errors['corporate_support_levels'] = self.error_class(['This field is required.'])

        # if simplified_membership_type == 'institutional' and not associate_consortium:
        #   self._errors['associate_consortium'] = self.error_class(['This field is required.'])

        # remove connected fields that are not active anymore
        if simplified_membership_type != 'corporate' and corporate_support_levels:
            del cleaned_data['corporate_support_levels']

        if simplified_membership_type != 'institutional' and associate_consortium:
            del cleaned_data['associate_consortium']

        return cleaned_data

    class Meta:
        model = MembershipApplication

class MemberLoginForm(forms.Form):
    organization = forms.ChoiceField()
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(MemberLoginForm, self).__init__(*args, **kwargs)
        self.fields['organization'].choices = [(x.id, x.display_name) for x in Organization.active.all()]

    def clean(self):
        cleaned_data = super(MemberLoginForm, self).clean()

        email = cleaned_data.get('email', '').strip()
        org = cleaned_data.get('organization')

        if org and email and not Organization.active.filter(pk=org, contact__email=email):
            raise forms.ValidationError('E-mail you entered is not associated with selected organization. Please contact members services if you require assistance.', code='invalid-email')

        return cleaned_data