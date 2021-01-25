# -*- coding: utf-8 -*-
from django import forms
from django.utils.safestring import mark_safe

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div, HTML

from .models import Candidate, EXPERTISE_CHOICES
from crm.models import Organization


class CandidateAddForm(forms.Form):
    candidate_first_name = forms.CharField(label="First name")
    candidate_last_name = forms.CharField(label="Last name")
    candidate_job_title = forms.CharField(label="Job title", required=False)
    candidate_email = forms.EmailField(label="E-mail")
    candidate_phone_number = forms.CharField(label="Phone number", required=False)

    reason = forms.CharField(
        widget=forms.Textarea,
        label="Reason for nomination",
        help_text="This may be used in consideration by the Nominating Committee but will not be displayed on the ballot. Candidates will be contacted to provide their own profile information for the ballot.",
    )
    organization = forms.ChoiceField(
        label="Member Institution this candidate represents"
    )

    sponsor_first_name = forms.CharField(label="First name")
    sponsor_last_name = forms.CharField(label="Last name")
    sponsor_email = forms.EmailField(label="E-mail")

    terms = forms.BooleanField(label="I have read the terms", required=True)
    expertise = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        label="Which of the following areas of expertise does nominee bring to the Board",
        choices=EXPERTISE_CHOICES,
    )
    expertise_other = forms.CharField(
        label='If you chose "Other" as area of expertise, please indicate it here',
        max_length=255,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(CandidateAddForm, self).__init__(*args, **kwargs)
        self.fields["organization"].choices = [
            (x.id, x.display_name) for x in Organization.active.all()
        ]

        self.helper = FormHelper(self)
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                HTML("<h2>Nominate a Candidate for Board of Directors</h2>"),
                css_class="row",
            ),
            Div(
                HTML("<h3>Nominee Information</h3>"),
                Field("candidate_first_name"),
                Field("candidate_last_name"),
                Field("candidate_job_title"),
                Field("candidate_email"),
                Field("candidate_phone_number"),
                Field("reason"),
                Div(
                    Field("expertise"), Field("expertise_other"), css_class="expertise"
                ),
                Field("organization"),
                css_class="row",
            ),
            Div(
                HTML("<h3>Submitter Information</h3>"),
                Field("sponsor_first_name"),
                Field("sponsor_last_name"),
                Field("sponsor_email"),
                css_class="row",
            ),
            Div(
                HTML(
                    """<h3>Terms and Conditions</h3>
                        <h4>General responsibilities of Board Members</h4>
                        <ul>
                            <li>The Board of Directors is charged with setting the strategic direction of Open Education Global.  Board members make high level decisions concerning the mission, outputs, finances and services of the Organization.  Board members are expected to act in the best interest of the organization and its members in all deliberations. </li>
                            <li>To fulfil its charge, the Board will hold four in meetings a year, two of which will be in person (situation permitting) and two online.</li>
                            <li>The Board member's institution is expected to cover the cost of the Board member's travel to meetings and time that is given to Open Education Global.</li>
                            <li>The Board, or its sub-committees, may decide to conduct some business by conference call between in-person meetings. While the frequency and amount of time required for these calls will depend on the nature of the business being conducted, one might anticipate that the Board itself would not normally meet by phone more than once a month.</li>
                            <li>Likewise, it is anticipated that Board members will serve as liaisons with various standing committees and work groups, and will represent the Organization from time to time at various meetings and/or events.</li>
                        </ul>
                    <p>I AM AWARE THAT BOARD MEMBERS EXPEND CONSIDERABLE NON-REIMBURSED TIME AND MONEY IN THE FULFILLMENT OF THEIR DUTIES. I ATTEST THAT I HAVE THE CONSENT OF THE NOMINEE IN THIS MATTER. I ALSO ATTEST THAT THE NOMINEE IS QUALIFIED AND ABLE TO SERVE IF ELECTED.</p>
                    <p><a href="https://www.oeconsortium.org/wp-content/uploads/2013/07/Bylaws_Open-Education_Consortium_Incorporated_-_March-1-2017.pdf" target="_blank">(See Open Education Global By-Laws Article III for qualification and responsibilities of Board Members).</a></p>
                    """
                ),
                css_class="row terms",
            ),
            Div(Field("terms"), css_class="row"),
        )
        self.helper.layout.append(Submit("Submit", "submit"))

    def clean_expertise_other(self):
        cleaned_data = self.cleaned_data

        if "5" in cleaned_data.get("expertise") and not cleaned_data.get(
            "expertise_other"
        ):
            raise forms.ValidationError("This is a required field", code="invalid")

        return cleaned_data.get("expertise_other")

    def clean_expertise(self):
        cleaned_data = self.cleaned_data

        return ",".join([i for i in cleaned_data.get("expertise", [])])


ACCEPTANCE_CHOICES = ((1, "I ACCEPT this nomination"), (0, "I DECLINE this nomination"))


class CandidateEditForm(forms.ModelForm):
    acceptance = forms.BooleanField(
        widget=forms.RadioSelect(choices=ACCEPTANCE_CHOICES),
        label="Acceptance of nomination",
    )
    expertise = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        label="Which of the following areas of expertise do you bring to the Board",
        choices=EXPERTISE_CHOICES,
    )
    expertise_other = forms.CharField(
        label='If you chose "Other" as area of expertise, please indicate it here',
        max_length=255,
        required=False,
    )

    agreement_cost = forms.BooleanField(
        label="I understand that The Board members institution is expected to cover the cost of the Board member's travel to meetings and time that is given to Open Education Global.",
        required=True,
    )
    agreement_fund = forms.BooleanField(
        label="I have verified with my institution that they will fund the costs associated with attending the two annual in person meetings of the OEG Board.",
        required=True,
    )

    def __init__(self, *args, **kwargs):
        instance = kwargs.get("instance")
        initial = {}
        if instance.status == "accepted":
            initial["acceptance"] = ACCEPTANCE_CHOICES[0][0]

        if instance.expertise:
            initial["expertise"] = instance.expertise.split(",")

        if initial:
            kwargs["initial"] = initial

        super(CandidateEditForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_show_errors = True

        self.fields["candidate_first_name"].label = "First name"
        self.fields["candidate_last_name"].label = "Last name"
        self.fields["candidate_job_title"].label = "Job title"
        self.fields["candidate_phone_number"].label = "Phone number"
        self.fields["candidate_email"].label = "Email"
        self.fields["email_alternate"].label = "Alternative e-mail"
        self.fields["organization"].label = "Institution you represent"

        for field in [
            "biography",
            "vision",
            "ideas",
            "expertise",
            "expertise_expanded",
        ]:
            self.fields[field].required = True

        self.fields[
            "biography"
        ].label = "Candidate Biography <br /><br />Please provide a brief summary of your experience and qualifications <br />This will be displayed on the ballot."
        self.fields[
            "vision"
        ].label = "Candidate Vision and Goals <br /><br />Please provide a brief list of what you hope to accomplish for Open Education Global if you are elected to the board of directors.  This will be displayed on the ballot."

        self.fields[
            "ideas"
        ].label = "Ideas for Open Education Global <br /><br />Please provide a brief description of your ideas for Open Education Global in general."
        self.fields[
            "expertise"
        ].label = "Your expertise and skills <br /><br />Please provide a brief description of expertise and skills (e.g. technical knowledge, financial knowledge, influence in public policy)."
        self.fields[
            "external_url"
        ].label = 'External Link <br /><br />You may optionally share a link to an external page such as a CV, blog or social networking profile page.  Please include the "http://" portion.'

        self.fields[
            "expertise_expanded"
        ].label = "Please provide a brief description of your expertise and skills with special reference to the areas of expertise check boxes you selected above"

        self.helper.layout = Layout(
            Div(
                HTML("<h2>Update Your Candidacy for Board of Directors</h2>"),
                HTML(
                    u"<p>You have been nominated as a candidate for Open Education Global Board of Directors by {instance.sponsor_first_name} {instance.sponsor_last_name}. <br /> Please review this page and complete any missing information to accept your nomination.</p>".format(
                        instance=instance
                    )
                ),
                css_class="row",
            ),
            Div(
                HTML("<h3>Personal Profile Information</h3>"),
                Field("candidate_first_name"),
                Field("candidate_last_name"),
                Field("candidate_job_title"),
                Field("candidate_email"),
                Field("email_alternate"),
                Field("candidate_phone_number"),
                Field("organization"),
                css_class="row",
            ),
            Div(
                HTML("<h3>Nominee Information</h3>"),
                Field("biography"),
                Field("vision"),
                Field("ideas"),
                Field("expertise"),
                Field("expertise_other"),
                Field("expertise_expanded"),
                Field("external_url"),
                css_class="row",
            ),
            Div(
                HTML(
                    """<h3>Terms and Conditions</h3>
                        <h4>General responsibilities of Board Members</h4>
                        <ul>
                            <li>The Board of Directors is charged with setting the strategic direction of Open Education Global.  Board members make high level decisions concerning the mission, outputs, finances and services of the Organization.  Board members are expected to act in the best interest of the organization and its members in all deliberations. </li>
                            <li>To fulfill its charge, the Board will hold four in meetings a year, two of which will be in person and two online. It is important that board members make every attempt to fully participate in all meetings.  While substitutions are permitted if necessary, the substitute will not be allowed to vote on the Board member's behalf.</li>
                            <li>The Board member's institution is expected to cover the cost of the Board member's travel to meetings and time that is given to Open Education Global.</li>
                            <li>The Board, or its sub-committees, may decide to conduct some business by conference call between in-person meetings. While the frequency and amount of time required for these calls will depend on the nature of the business being conducted, one might anticipate that the Board itself would not normally meet by phone more than once a month.</li>
                            <li>Likewise, it is anticipated that Board members will serve as liaisons with various standing committees and work groups, and will represent the Organization from time to time at various meetings and/or events.</li>
                        </ul>
                    <p>I AM AWARE THAT BOARD MEMBERS EXPEND CONSIDERABLE NON-REIMBURSED TIME AND MONEY IN THE FULFILLMENT OF THEIR DUTIES.  I ATTEST THAT I AM QUALIFIED AND ABLE TO SERVE IF ELECTED.</p>
                    <p><a href="https://www.oeconsortium.org/wp-content/uploads/2013/07/Bylaws_Open-Education_Consortium_Incorporated_-_March-1-2017.pdf" target="_blank">(See Open Education Global By-Laws Article III for qualification and responsibilities of Board Members).</a></p>
                    """
                ),
                Field("agreement_cost"),
                Field("agreement_fund"),
                css_class="row terms",
            ),
            Div(Field("acceptance"), css_class="row"),
        )

        self.helper.layout.append(
            Submit("submit", "Update my Candidacy for Board of Directors")
        )

    def save(self, *args, **kwargs):
        candidate = super(CandidateEditForm, self).save(*args, **kwargs)
        if self.cleaned_data.get("acceptance"):
            candidate.status = "accepted"
            candidate.save()
        return candidate

    def clean_expertise_other(self):
        cleaned_data = self.cleaned_data

        if "5" in cleaned_data.get("expertise") and not cleaned_data.get(
            "expertise_other"
        ):
            raise forms.ValidationError("This is a required field", code="invalid")

        return cleaned_data.get("expertise_other")

    def clean_expertise(self):
        cleaned_data = self.cleaned_data

        return ",".join([i for i in cleaned_data.get("expertise", [])])

    class Meta:
        model = Candidate
        fields = [
            "candidate_first_name",
            "candidate_last_name",
            "candidate_job_title",
            "candidate_email",
            "candidate_phone_number",
            "organization",
            "email_alternate",
            "biography",
            "vision",
            "ideas",
            "expertise",
            "expertise_other",
            "expertise_expanded",
            "external_url",
            "agreement_cost",
            "agreement_fund",
            "acceptance",
        ]


PROPOSITION_CHOICES = (
    ("yes", mark_safe("We vote <strong>for</strong> this proposition")),
    ("no", mark_safe("We vote <strong>against</strong> this proposition")),
    ("abstain", mark_safe("We abstain")),
)


class VoteForm(forms.Form):
    # proposition_vote1 = forms.ChoiceField(widget=forms.RadioSelect, label="We vote", choices=PROPOSITION_CHOICES)
    # proposition_vote2 = forms.ChoiceField(widget=forms.RadioSelect, label="We vote", choices=PROPOSITION_CHOICES)
    # proposition_vote3 = forms.ChoiceField(widget=forms.RadioSelect, label="We vote", choices=PROPOSITION_CHOICES)
    # proposition_vote4 = forms.ChoiceField(widget=forms.RadioSelect, label="We vote", choices=PROPOSITION_CHOICES)
    # proposition_vote5 = forms.ChoiceField(widget=forms.RadioSelect, label="We vote", choices=PROPOSITION_CHOICES)
    # proposition_vote6 = forms.ChoiceField(widget=forms.RadioSelect, label="We vote", choices=PROPOSITION_CHOICES)

    institutional_candidates = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        label="Select 5 Candidates for Board of Directors, Institutional Seats",
    )

    name = forms.CharField(
        label="Please enter your First and Last name, to sign your vote on behalf of your organization"
    )

    def __init__(self, *args, **kwargs):
        self.election = kwargs.pop("election")
        super(VoteForm, self).__init__(*args, **kwargs)

        self.fields["institutional_candidates"].choices = [
            (i.id, unicode(i))
            for i in self.election.candidate_set.filter(
                vetted=True, seat_type="institutional"
            ).order_by("order")
        ]

        self.helper = FormHelper(self)
        self.helper.form_show_errors = True

        propositions = self.election.proposition_set.filter(published=True).order_by(
            "title"
        )
        # proposition1 = propositions[0]
        # proposition2 = propositions[1]
        # proposition3 = propositions[2]
        # proposition4 = propositions[3]
        # proposition5 = propositions[4]
        # proposition6 = propositions[5]

        self.helper.layout = Layout(
            Div(HTML("<h2>2020 Open Education Global Elections</h2>"), css_class="row"),
            # Div(
            #     HTML('<div class="large-8 columns">Please see the background information on the Proposed bylaws changes for an explanation of these proposed changes, and then vote on each issue below. <br /></br ><a target="_blank" style="font-weight: bold;" href="https://docs.google.com/document/d/1Hszn22Iu5GTtEalvRDpVNDOTYOfoO6DA8vFhYP-kWyo/edit">Click here for background information</a>.<br /><br /></div>'),
            #     css_class='row'
            # ),
            Div(HTML("<p>Fields marked with * are mandatory</p>"), css_class="row"),
            # Div(
            #     HTML("<h4>%s</h4>" % proposition1.title),
            #     HTML("<p>%s</p>" % proposition1.description),
            #     css_class='row'),
            # Div(
            #     Field('proposition_vote1'),
            #     css_class='row'),
            #
            # Div(
            #     HTML("<h4>%s</h4>" % proposition2.title),
            #     HTML("<p>%s</p>" % proposition2.description),
            #     css_class='row'),
            # Div(
            #     Field('proposition_vote2'),
            #     css_class='row'),
            #
            # Div(
            #     HTML("<h4>%s</h4>" % proposition3.title),
            #     HTML("<p>%s</p>" % proposition3.description),
            #     css_class='row'),
            # Div(
            #     Field('proposition_vote3'),
            #     css_class='row'),
            #
            # Div(
            #     HTML("<h4>%s</h4>" % proposition4.title),
            #     HTML("<p>%s</p>" % proposition4.description),
            #     css_class='row'),
            # Div(
            #     Field('proposition_vote4'),
            #     css_class='row'),
            #
            # Div(
            #     HTML("<h4>%s</h4>" % proposition5.title),
            #     HTML("<p>%s</p>" % proposition5.description),
            #     css_class='row'),
            # Div(
            #     Field('proposition_vote5'),
            #     css_class='row'),
            #
            # Div(
            #     HTML("<h4>%s</h4>" % proposition6.title),
            #     HTML("<p>%s</p>" % proposition6.description),
            #     css_class='row'),
            # Div(
            #     Field('proposition_vote6'),
            #     css_class='row'),
            Div(
                HTML(
                    "<p>Open Education Global by-laws require us to have 10 Board of Directors chosen by members. This year we need to "
                    "elect 5 new Board members. To ensure we get the necessary 5 new Board members we ask OEG members to cast all 5 "
                    "votes. This will also help ensure we get a diverse and inclusive Board with representation from around the world. <br /><br />To "
                    "inform your decision making about who to vote for we invite you to review the information about each candidate "
                    'at <a href="https://www.oeglobal.org/about-us/elections/" target="_blank">https://www.oeglobal.org/about-us/elections/</a></p>'
                ),
                css_class="row",
            ),
            Div(Field("institutional_candidates"), css_class="row"),
            # Div(
            #     Field('organizational_candidates'),
            #     css_class='row'),
            Div(Field("name"), css_class="row"),
        )
        self.helper.layout.append(Submit("submit", "Submit"))

    def clean(self):
        cleaned_data = self.cleaned_data

        if (
            self.cleaned_data.get("institutional_candidates")
            and len(self.cleaned_data.get("institutional_candidates")) != 5
        ):
            self._errors["institutional_candidates"] = self.error_class(
                ["Please select 5 candidates."]
            )

        return cleaned_data
