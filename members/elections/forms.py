# -*- coding: utf-8 -*-
from django import forms
from django.utils.safestring import mark_safe

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div, HTML

from .models import Candidate, Election, Proposition
from crm.models import Organization

class CandidateAddForm(forms.Form):
    candidate_first_name = forms.CharField(label='First name')
    candidate_last_name = forms.CharField(label='Last name')
    candidate_job_title = forms.CharField(label='Job title', required=False)
    candidate_email = forms.EmailField(label='E-mail')
    candidate_phone_number = forms.CharField(label='Phone number', required=False)

    reason = forms.CharField(widget=forms.Textarea, label='Reason for nomination',
                            help_text='This may be used in consideration by the Nominating Committee but will not be displayed on the ballot. Candidates will be contacted to provide their own profile information for the ballot.')
    organization = forms.ChoiceField(label='Member Institution this candidate represents')

    sponsor_first_name = forms.CharField(label='First name')
    sponsor_last_name = forms.CharField(label='Last name')
    sponsor_email = forms.EmailField(label='E-mail')

    terms = forms.BooleanField(label='I have read the terms', required=True)

    def __init__(self, *args, **kwargs):
        super(CandidateAddForm, self).__init__(*args, **kwargs)
        self.fields['organization'].choices = [(x.id, x.display_name) for x in Organization.active.all()]

        self.helper = FormHelper(self)
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                HTML('<h2>Nominate a Candidate for Board of Directors</h2>'),
            css_class='row'),
            Div(
                HTML('<h3>Nominee Information</h3>'),
                Field('candidate_first_name'),
                Field('candidate_last_name'),
                Field('candidate_job_title'),
                Field('candidate_email'),
                Field('candidate_phone_number'),
                Field('reason'),
                Field('organization'),
            css_class='row'),
            Div(
                HTML('<h3>Submitter Information</h3>'),
                Field('sponsor_first_name'),
                Field('sponsor_last_name'),
                Field('sponsor_email'),
            css_class='row'),
            Div(HTML('''<h3>Terms and Conditions</h3>
                        <h4>General responsibilities of Board Members</h4>
                        <ul>
                            <li>The Board of Directors is charged with setting the strategic direction of the OCW Consortium.  Board members make high level decisions concerning the mission, outputs, finances and services of the Consortium.  Board members are expected to act in the best interest of the organization and its members in all deliberations. </li>
                            <li>To fulfill its charge, the Board will hold four in meetings a year, two of which will be in person and two online. It is important that board members make every attempt to fully participate in all meetings.  While substitutions are permitted if necessary, the substitute will not be allowed to vote on the Board member's behalf.</li>
                            <li>The Board member's institution is expected to cover the cost of the Board member's travel to meetings and time that is given to the OCW Consortium.  The OCWC does have some funds for defraying some, but not all, expenses of Board members traveling to these meetings which can be requested for members coming from under resourced institutions, or other exceptional circumstances.</li>
                            <li>The Board, or its sub-committees, may decide to conduct some business by conference call between in-person meetings. While the frequency and amount of time required for these calls will depend on the nature of the business being conducted, one might anticipate that the Board itself would not normally meet by phone more than once a month.</li>
                            <li>Likewise, it is anticipated that Board members will serve as liaisons with various standing committees and work groups, and will represent the Consortium from time to time at various meetings and/or events.</li>
                        </ul>
                    <p>I AM AWARE THAT BOARD MEMBERS EXPEND CONSIDERABLE NON-REIMBURSED TIME AND MONEY IN THE FULFILLMENT OF THEIR DUTIES.  I ATTEST THAT I HAVE THE CONSENT OF THE NOMINEE IN THIS MATTER. I ALSO ATTEST THAT THE NOMINEE IS QUALIFIED AND ABLE TO SERVE IF ELECTED.</p>
                    <p><a href="http://www.ocwconsortium.org/wp-content/uploads/2014/02/Bylaws_OpenCourseWare_Consortium_Incorporated_-_April-20-2012.doc" target="_blank">(See OCWC By-Laws Article III for qualification and responsibilities of Board Members).</a></p>
                    '''
                ),
            css_class='row terms'),
            Div(
                Field('terms'),
            css_class='row')
        )
        self.helper.layout.append(Submit('Submit', 'submit'))

ACCEPTANCE_CHOICES =(
    (1, 'I ACCEPT this nomination'),
    (0, 'I DECLINE this nomination')
)

class CandidateEditForm(forms.ModelForm):
    acceptance = forms.BooleanField(widget=forms.RadioSelect(
                                    choices=ACCEPTANCE_CHOICES), label='Acceptance of nomination')

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance.status == 'accepted':
            kwargs['initial'] = {'acceptance': ACCEPTANCE_CHOICES[0][0] }

        super(CandidateEditForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_show_errors = True

        self.fields['candidate_first_name'].label = 'First name'
        self.fields['candidate_last_name'].label = 'Last name'
        self.fields['candidate_job_title'].label = 'Job title'
        self.fields['candidate_phone_number'].label = 'Phone number'
        self.fields['candidate_email'].label = 'Email'
        self.fields['email_alternate'].label = 'Alternative e-mail'
        self.fields['organization'].label = 'Institution you represent'

        self.fields['biography'].label = 'Candidate Biography <br /><br />Please provide a brief summary of your experience and qualifications <br />This will be displayed on the ballot.'
        self.fields['vision'].label = 'Candidate Vision and Goals <br /><br />Please provide a brief list of what you hope to accomplish for the OCWC if you are elected to the board of directors.  This will be displayed on the ballot.'

        self.fields['ideas'].label = 'Ideas for OpenCoursware Consortium <br /><br />Please provide a brief description of your ideas for OpenCoursware Consortium in general.'
        self.fields['expertise'].label = 'Your expertise and skills <br /><br />Please provide a brief description of expertise and skills (e.g. technical knowledge, financial knowledge, influence in public policy).'
        self.fields['external_url'].label = 'External Link <br /><br />You may optionally share a link to an external page such as a CV, blog or social networking profile page.  Please include the "http://" portion.'

        self.helper.layout = Layout(
            Div(
                HTML('<h2>Update Your Candidacy for Board of Directors</h2>'),
                HTML('<p>You have been nominated as a candidate for the OCW Consortium Board of Directors by {instance.sponsor_first_name} {instance.sponsor_last_name}. <br /> Please review this page and complete any missing information to accept your nomination.</p>'.format(instance=instance)),
            css_class='row'),
            Div(
                HTML('<h3>Personal Profile Information</h3>'),
                Field('candidate_first_name'),
                Field('candidate_last_name'),
                Field('candidate_job_title'),
                Field('candidate_email'),
                Field('email_alternate'),
                Field('candidate_phone_number'),
                Field('organization'),
            css_class='row'),
            Div(
                HTML('<h3>Nominee Information</h3>'),
                Field('biography'),
                Field('vision'),
                Field('ideas'),
                Field('expertise'),
                Field('external_url'),
            css_class='row'),
            Div(HTML('''<h3>Terms and Conditions</h3>
                        <h4>General responsibilities of Board Members</h4>
                        <ul>
                            <li>The Board of Directors is charged with setting the strategic direction of the OCW Consortium.  Board members make high level decisions concerning the mission, outputs, finances and services of the Consortium.  Board members are expected to act in the best interest of the organization and its members in all deliberations. </li>
                            <li>To fulfill its charge, the Board will hold four in meetings a year, two of which will be in person and two online. It is important that board members make every attempt to fully participate in all meetings.  While substitutions are permitted if necessary, the substitute will not be allowed to vote on the Board member's behalf.</li>
                            <li>The Board member's institution is expected to cover the cost of the Board member's travel to meetings and time that is given to the OCW Consortium.  The OCWC does have some funds for defraying some, but not all, expenses of Board members traveling to these meetings which can be requested for members coming from under resourced institutions, or other exceptional circumstances.</li>
                            <li>The Board, or its sub-committees, may decide to conduct some business by conference call between in-person meetings. While the frequency and amount of time required for these calls will depend on the nature of the business being conducted, one might anticipate that the Board itself would not normally meet by phone more than once a month.</li>
                            <li>Likewise, it is anticipated that Board members will serve as liaisons with various standing committees and work groups, and will represent the Consortium from time to time at various meetings and/or events.</li>
                        </ul>
                    <p>I AM AWARE THAT BOARD MEMBERS EXPEND CONSIDERABLE NON-REIMBURSED TIME AND MONEY IN THE FULFILLMENT OF THEIR DUTIES.  I ATTEST THAT I AM QUALIFIED AND ABLE TO SERVE IF ELECTED.</p>
                    <p><a href="http://www.ocwconsortium.org/wp-content/uploads/2014/02/Bylaws_OpenCourseWare_Consortium_Incorporated_-_April-20-2012.doc" target="_blank">(See OCWC By-Laws Article III for qualification and responsibilities of Board Members).</a></p>
                    '''
                ),
            css_class='row terms'),
            Div(
                Field('acceptance'),
            css_class='row')
        )

        self.helper.layout.append(Submit('submit', 'Update my Candidacy for Board of Directors'))

    def save(self, *args, **kwargs):
        candidate = super(CandidateEditForm, self).save(*args, **kwargs)
        if self.cleaned_data.get('acceptance'):
            candidate.status = 'accepted'
            candidate.save()
        return candidate

    class Meta:
        model = Candidate
        fields = ['candidate_first_name', 'candidate_last_name', 'candidate_job_title', 'candidate_email',
                  'candidate_phone_number', 'organization', 'email_alternate',
                  'biography', 'vision', 'ideas', 'expertise', 'external_url', 'acceptance']

PROPOSITION_CHOICES = (
    ('yes', mark_safe('We vote <strong>for</strong> this proposition')),
    ('no', mark_safe('We vote <strong>against</strong> this proposition')),
    ('abstain', mark_safe('We abstain')),
)

class VoteForm(forms.Form):
    proposition_vote = forms.ChoiceField(widget=forms.RadioSelect,
                                         label="We vote", choices=PROPOSITION_CHOICES)
    institutional_candidates = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, label="Select up to 4 Candidates for Board of Directors, Institutional Seats")
    organizational_candidates = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, label="Select 1 candidate for Board of Directors, Organizational Seat")
    name = forms.CharField(label="Please enter your First and Last name, to sign your vote on behalf of your organization")

    def __init__(self, *args, **kwargs):
        self.election = kwargs.pop('election')
        super(VoteForm, self).__init__(*args, **kwargs)

        self.fields['institutional_candidates'].choices = [ (i.id, unicode(i)) for i in self.election.candidate_set.filter(vetted=True, seat_type='institutional').order_by('candidate_last_name') ]
        self.fields['organizational_candidates'].choices = [ (i.id, unicode(i)) for i in self.election.candidate_set.filter(vetted=True, seat_type='organizational').order_by('candidate_last_name') ]

        self.helper = FormHelper(self)
        self.helper.form_show_errors = True

        proposition = Proposition.objects.last()

        self.helper.layout = Layout(
            Div(
                HTML('<h2>2014 OpenCoursWare Consortium Elections</h2>'),
            css_class='row'),
            Div(
                HTML("<h2>%s</h2>" % proposition.title),
                HTML("<p>%s</p>" % proposition.description),
            css_class='row'),
            Div(
                Field('proposition_vote'),
            css_class='row'),
            Div(
                Field('institutional_candidates'),
            css_class='row'),
            Div(
                Field('organizational_candidates'),
            css_class='row'),
            Div(
                Field('name'),
            css_class='row'),
        )
        self.helper.layout.append(Submit('submit', 'Submit'))

    def clean(self):
        cleaned_data = self.cleaned_data

        if len(self.cleaned_data.get('institutional_candidates')) > 4:
            self._errors['institutional_candidates'] = self.error_class(['Too many candidates selected.'])

        if len(self.cleaned_data.get('organizational_candidates')) > 1:
            self._errors['organizational_candidates'] = self.error_class(['Too many candidates selected.'])

        return cleaned_data