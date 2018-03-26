# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail

from elections.models import Election, CandidateBallot
from crm.models import Contact, Organization, LoginKey


class Command(BaseCommand):
    help = "send emails with login keys to members that haven't voted yet"

    def handle(self, *args, **options):
        for org in Organization.objects.filter(membership_status__in=[2, 5, 7]):
            election = Election.objects.latest('id')

            if CandidateBallot.objects.filter(election=election, organization=org).exists():
                continue

            emails = []
            seen_emails = []
            for contact in Contact.objects.filter(organization=org, bouncing=False).exclude(contact_type=13):
                if contact.email not in seen_emails:
                    emails.append(contact)
                    seen_emails.append(contact.email)

            key = LoginKey(user=org.user, email=contact.email)
            key.save()

            for contact in emails:
                body = render_to_string('elections/email_vote_mailing.txt', {
                    'url': key.get_absolute_url(),
                    'contact': contact
                })
                send_mail('Last chance to vote in OEC 2018 Elections!', body,
                          'memberservices@oeconsortium.org', [contact.email])
