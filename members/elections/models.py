# -*- coding: utf-8 -*-
import uuid

from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse

from crm.models import Organization

class Election(models.Model):
    title = models.CharField(max_length=255)
    view_nominations_key = models.CharField(max_length=255, blank=True)
    edit_nominations_key = models.CharField(max_length=255, blank=True)

    nominate_until = models.DateTimeField(null=True)
    vote_from = models.DateTimeField(null=True)
    vote_until = models.DateTimeField(null=True)

    def save(self, force_insert=False, force_update=False, using=None):
        if not self.view_nominations_key:
            self.view_nominations_key = uuid.uuid4().get_hex()
        if not self.edit_nominations_key:
            self.edit_nominations_key = uuid.uuid4().get_hex()
        super(Election, self).save(force_insert=force_insert, force_update=force_update, using=using)


CANDIDATE_STATUS_CHOICES = (
    ('nominated', 'Nominated'),
    ('accepted', 'Accepted'),
    ('declined', 'Declined'),
    ('rejected', 'Rejected'),
    ('spam', 'Spam')
)

SEAT_TYPE_CHOICES = (
    ('institutional', 'Institutional'),
    ('organizational', 'Organizational')
)

class Candidate(models.Model):
    election = models.ForeignKey(Election)
    status = models.CharField(max_length=60, choices=CANDIDATE_STATUS_CHOICES, default='')

    candidate_first_name = models.CharField(max_length=255)
    candidate_last_name = models.CharField(max_length=255)
    candidate_job_title = models.CharField(max_length=255, blank=True, default='')
    candidate_email = models.EmailField(max_length=255)
    candidate_phone_number = models.CharField(max_length=255, blank=True, default='')

    reason = models.TextField(blank=True)
    # organization = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization)

    sponsor_first_name = models.CharField(max_length=255)
    sponsor_last_name = models.CharField(max_length=255)
    sponsor_email = models.CharField(max_length=255)

    edit_link_key = models.CharField(max_length=255, blank=True)
    view_link_key = models.CharField(max_length=255, blank=True)

    email_alternate = models.CharField(max_length=255, blank=True, default='')
    biography = models.TextField(blank=True)
    vision = models.TextField(blank=True)
    ideas = models.TextField(blank=True)
    expertise = models.TextField(blank=True)
    external_url = models.CharField(max_length=255, blank=True, default='')

    vetted = models.BooleanField(default=False)
    seat_type = models.CharField(max_length=60, choices=SEAT_TYPE_CHOICES, blank=True)

    pub_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def get_absolute_edit_url(self):
        return reverse('elections:candidate-edit', kwargs={'key':self.edit_link_key})

    def save(self, force_insert=False, force_update=False, using=None):
        if not self.edit_link_key:
            self.edit_link_key = uuid.uuid4().get_hex()
        if not self.view_link_key:
            self.view_link_key = uuid.uuid4().get_hex()
        super(Candidate, self).save(force_insert=force_insert, force_update=force_update, using=using)

    def email_board(self):
        send_mail(u"{candidate.candidate_first_name} {candidate.candidate_last_name} was nominated for OCWC board".format(candidate=self),
                  render_to_string('elections/email_candidate_board_body.txt', {'candidate': self}),
                  'tech@ocwconsortium.org', [settings.NOMINATION_COMMITTEE_EMAIL]
        )

    def email_candidate(self):
        send_mail(u"You have been nominated to serve on the OCWC Board of Directors",
                  render_to_string('elections/email_candidate_nominee_body.txt', {'candidate': self}),
                  'tech@ocwconsortium.org', [self.candidate_email]
        )

    def __unicode__(self):
        return "%s %s (%s)" % (self.candidate_first_name, self.candidate_last_name, self.organization.display_name)

class CandidateBallot(models.Model):
    election = models.ForeignKey(Election)
    organization = models.ForeignKey(Organization)
    voter_name = models.CharField(max_length=255)

    seat_type = models.CharField(max_length=60, choices=SEAT_TYPE_CHOICES)
    votes = models.ManyToManyField(Candidate)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

class Proposition(models.Model):
    election = models.ForeignKey(Election)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    published = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

class PropositionBallot(models.Model):
    election = models.ForeignKey(Election)
    organization = models.ForeignKey(Organization)
    voter_name = models.CharField(max_length=255)

    vote = models.NullBooleanField(null=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
