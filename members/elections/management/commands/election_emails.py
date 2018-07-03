# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.conf import settings

from elections.models import Election, CandidateBallot
from crm.models import Contact, Organization


class Command(BaseCommand):
    help = "updates mailgun with emails of orgs that didn't vote yet"

    def handle(self, *args, **options):
        for org in Organization.objects.filter(membership_status__in=[2, 5, 7]):
            election = Election.objects.latest('id')

            if CandidateBallot.objects.filter(election=election, organization=org).exists():
                continue

            for contact in Contact.objects.filter(organization=org,
                                                  bouncing=False,
                                                  contact_type__in=(4, 6, 9, 10, 11, 12)):
                print(contact.email)
