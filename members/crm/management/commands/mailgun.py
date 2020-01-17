# -*- coding: utf-8 -*-
import requests
import json
import arrow
from pprint import pprint

from django.core.management.base import BaseCommand
from django.conf import settings

from crm.models import Contact


class Command(BaseCommand):
    help = "tools to manage our mailgun email subscriptions"

    def add_arguments(self, parser):
        parser.add_argument(
            "--get-bounces",
            action="store_true",
            dest="get_bounces",
            help="Downloads bounces and updates Contact record",
        )
        parser.add_argument(
            "--update-list",
            action="store_true",
            dest="update_list",
            help="Updates members announce mailing list",
        )

    def handle(self, *args, **options):
        if options.get("get_bounces"):
            self.get_bounces()
        if options.get("update_list"):
            self.update_list()
            self.update_list("sustaining-list", (7,))
            self.update_list("leadcontacts-list", contact_type=(6,))
            self.update_list("allcontacts-list", contact_type=(4, 6, 9, 10, 11, 12, 13))

    def get_bounces(self):
        r = requests.get(
            "https://api.mailgun.net/v2/oeconsortium.org/bounces",
            auth=("api", settings.MAILGUN_APIKEY),
        )
        data = json.loads(r.content)
        for bounce in data["items"]:
            for contact in Contact.objects.filter(
                email__iexact=bounce.get("address"), bouncing=False
            ):
                contact.bouncing = True
                contact.save()

                self.stdout.write(
                    u"Marking {contact.email} as bouncing - {contact.first_name} {contact.last_name} from {contact.organization.display_name}".format(
                        contact=contact
                    )
                )

        r = requests.get(
            "https://api.mailgun.net/v2/oeconsortium.org/events",
            auth=("api", settings.MAILGUN_APIKEY),
            params={
                "begin": arrow.now()
                .replace(weeks=-1)
                .strftime("%a, %d %b %Y %H:%M:%S +0000"),
                "end": arrow.now().strftime("%a, %d %b %Y %H:%M:%S +0000"),
                "event": "failed",
            },
        )
        data = json.loads(r.content)
        for bounce in data["items"]:
            if bounce.get("severity") == "permanent":
                for contact in Contact.objects.filter(
                    email__iexact=bounce.get("recipient"), bouncing=False
                ):
                    contact.bouncing = True
                    contact.save()

                    self.stdout.write(
                        u"Marking {contact.email} as bouncing - {contact.first_name} {contact.last_name} from {contact.organization.display_name}".format(
                            contact=contact
                        )
                    )

    def update_list(
        self,
        list_name="members-list",
        membership_status=(2, 3, 5, 7, 99),
        contact_type=(4, 6, 9, 10, 11, 12),
    ):
        offset = 0

        emails = []
        while True:
            r = requests.get(
                "https://api.mailgun.net/v2/lists/{0}@oeglobal.org/members".format(
                    list_name
                ),
                auth=("api", settings.MAILGUN_APIKEY),
                data={"skip": offset},
            )

            data = json.loads(r.content)

            if not data["items"]:
                break

            for mailing_member in data["items"]:
                email = mailing_member.get("address").lower()
                if email not in emails:
                    emails.append(email)
                if Contact.objects.filter(email__iexact=email, bouncing=True).exists():
                    r = requests.delete(
                        "https://api.mailgun.net/v2/lists/{0}@oeglobal.org/members/".format(
                            list_name
                        )
                        + mailing_member.get("address"),
                        auth=("api", settings.MAILGUN_APIKEY),
                    )
                    d = json.loads(r.content)
                    print("Deleting:", d.get("member").get("address"), d.get("message"))

            offset += 100

        self.stdout.write("New emails:")
        for contact in Contact.objects.filter(
            contact_type__in=contact_type,
            organization__membership_status__in=membership_status,
            bouncing=False,
        ):
            email = contact.email.lower()
            if email not in emails:
                r = requests.post(
                    "https://api.mailgun.net/v2/lists/{0}@oeglobal.org/members".format(
                        list_name
                    ),
                    params={"address": email},
                    auth=("api", settings.MAILGUN_APIKEY),
                )
                d = json.loads(r.content)
                print("Added:", email, d)

        # remove emails from people that are in canceled organizations
        for contact in Contact.objects.filter(contact_type__in=contact_type).exclude(
            organization__membership_status__in=membership_status
        ):
            email = contact.email.lower()
            if (
                email in emails
                and not Contact.objects.filter(
                    organization__membership_status__in=membership_status,
                    email__iexact=email,
                ).count()
            ):
                r = requests.delete(
                    "https://api.mailgun.net/v2/lists/{0}@oeglobal.org/members/".format(
                        list_name
                    )
                    + email,
                    auth=("api", settings.MAILGUN_APIKEY),
                )
                d = json.loads(r.content)
                print(
                    "Deleting canceled membership contact:",
                    d.get("member", {}).get("address"),
                    d.get("message"),
                )

        for email in emails:
            if not Contact.objects.filter(email__iexact=email).exists():
                if email.endswith("@oeglobal.org"):
                    continue

                r = requests.delete(
                    "https://api.mailgun.net/v2/lists/{0}@oeglobal.org/members/".format(
                        list_name
                    )
                    + email,
                    auth=("api", settings.MAILGUN_APIKEY),
                )
                d = json.loads(r.content)
                print("Deleting removed member email:", email, d.get("message"))
