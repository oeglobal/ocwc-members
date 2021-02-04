# -*- coding: utf-8 -*-
import uuid

from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.core.validators import validate_comma_separated_integer_list

from crm.models import Organization


class Election(models.Model):
    title = models.CharField(max_length=255)
    view_nominations_key = models.CharField(max_length=255, blank=True)
    edit_nominations_key = models.CharField(max_length=255, blank=True)

    nominate_until = models.DateTimeField(null=True)
    vote_from = models.DateTimeField(null=True)
    vote_until = models.DateTimeField(null=True)

    class Meta:
        get_latest_by = "pk"

    def save(self, force_insert=False, force_update=False, using=None):
        if not self.view_nominations_key:
            self.view_nominations_key = uuid.uuid4().hex
        if not self.edit_nominations_key:
            self.edit_nominations_key = uuid.uuid4().hex
        super(Election, self).save(
            force_insert=force_insert, force_update=force_update, using=using
        )

    def __str__(self):
        return self.title


CANDIDATE_STATUS_CHOICES = (
    ("nominated", "Nominated"),
    ("accepted", "Accepted"),
    ("declined", "Declined"),
    ("rejected", "Rejected"),
    ("spam", "Spam"),
)

SEAT_TYPE_CHOICES = (
    ("institutional", "Institutional"),
    ("organizational", "Organizational"),
)

EXPERTISE_CHOICES = (
    (1, "Fundraising & Sustainability"),
    (2, "Membership Growth and Engagement"),
    (3, "Events and Services"),
    (4, "Operations including Legal & Finance"),
    (5, "Other"),
)


class Candidate(models.Model):
    election = models.ForeignKey(Election, models.CASCADE)
    status = models.CharField(
        max_length=60, choices=CANDIDATE_STATUS_CHOICES, default=""
    )

    candidate_first_name = models.CharField(max_length=255)
    candidate_last_name = models.CharField(max_length=255)
    candidate_job_title = models.CharField(max_length=255, blank=True, default="")
    candidate_email = models.EmailField(max_length=255)
    candidate_phone_number = models.CharField(max_length=255, blank=True, default="")

    reason = models.TextField(blank=True)
    # organization = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, models.CASCADE)

    sponsor_first_name = models.CharField(max_length=255)
    sponsor_last_name = models.CharField(max_length=255)
    sponsor_email = models.CharField(max_length=255)

    edit_link_key = models.CharField(max_length=255, blank=True)
    view_link_key = models.CharField(max_length=255, blank=True)

    email_alternate = models.CharField(max_length=255, blank=True, default="")
    biography = models.TextField(blank=True)
    vision = models.TextField(blank=True)
    ideas = models.TextField(blank=True)

    external_url = models.CharField(max_length=255, blank=True, default="")

    vetted = models.BooleanField(default=False)
    seat_type = models.CharField(max_length=60, choices=SEAT_TYPE_CHOICES, blank=True)

    pub_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    order = models.IntegerField(default=0)

    expertise = models.TextField(
        default="", validators=[validate_comma_separated_integer_list], blank=True
    )
    expertise_other = models.CharField(default="", max_length=255, blank=True)
    expertise_expanded = models.TextField(default="", blank=True)

    agreement_cost = models.BooleanField(default=False)
    agreement_fund = models.BooleanField(default=False)

    def get_absolute_edit_url(self):
        return reverse("elections:candidate-edit", kwargs={"key": self.edit_link_key})

    def save(self, force_insert=False, force_update=False, using=None):
        if not self.edit_link_key:
            self.edit_link_key = uuid.uuid4().hex
        if not self.view_link_key:
            self.view_link_key = uuid.uuid4().hex
        super(Candidate, self).save(
            force_insert=force_insert, force_update=force_update, using=using
        )

    def email_board(self):
        send_mail(
            u"{candidate.candidate_first_name} {candidate.candidate_last_name} was nominated for OEG board".format(
                candidate=self
            ),
            render_to_string(
                "elections/email_candidate_board_body.txt", {"candidate": self}
            ),
            "tech@oeglobal.org",
            [settings.NOMINATION_COMMITTEE_EMAIL],
        )

    def email_candidate(self):
        send_mail(
            u"You have been nominated to serve on the OEG Board of Directors",
            render_to_string(
                "elections/email_candidate_nominee_body.txt", {"candidate": self}
            ),
            "tech@oeglobal.org",
            [self.candidate_email],
        )

    def get_expertise_items(self):
        expertise_list = self.expertise.split(",")
        choices = dict(EXPERTISE_CHOICES)
        items = []
        for expertise in expertise_list:
            items.append(choices[int(expertise)])

        return items

    def __str__(self):
        return "%s %s (%s)" % (
            self.candidate_first_name,
            self.candidate_last_name,
            self.organization.display_name,
        )


class CandidateBallot(models.Model):
    election = models.ForeignKey(Election, models.CASCADE)
    organization = models.ForeignKey(Organization, models.CASCADE)
    voter_name = models.CharField(max_length=255)

    seat_type = models.CharField(max_length=60, choices=SEAT_TYPE_CHOICES)
    votes = models.ManyToManyField(Candidate)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Proposition(models.Model):
    election = models.ForeignKey(Election, models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    published = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title


PROPOSITION_CHOICES = (
    (True, mark_safe("We vote <strong>for</strong> this proposition")),
    (False, mark_safe("We vote <strong>against</strong> this proposition")),
    (None, mark_safe("We abstain")),
)


class PropositionBallot(models.Model):
    election = models.ForeignKey(Election, models.CASCADE)
    proposition = models.ForeignKey(Proposition, models.CASCADE)

    organization = models.ForeignKey(Organization, models.CASCADE)
    voter_name = models.CharField(max_length=255)

    vote = models.NullBooleanField(null=True, choices=PROPOSITION_CHOICES)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
