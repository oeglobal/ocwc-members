# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from crm.models import Contact


class Command(BaseCommand):
    help = "generates a list of emails with Lead Contact, Certifier and Voting representatives"

    def handle(self, *args, **options):
        address_list = []

        for contact in Contact.objects.filter(
            organization__membership_status__in=(2, 3, 5, 7, 99), bouncing=False
        ).exclude(contact_type=13):

            if contact.email and contact.email not in address_list:
                address_list.append(
                    [contact.email, contact.organization.associate_consortium or ""]
                )

        for email in address_list:
            print("{},{}".format(*email))
