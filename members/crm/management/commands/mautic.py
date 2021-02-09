import requests
import json
import arrow
from pprint import pprint
from scalpl import Cut

from django.core.management.base import BaseCommand
from django.conf import settings

from crm.models import Contact


class Command(BaseCommand):
    help = "tools to manage our mautic email subscriptions"
    API_URL = settings.MAUTIC_API
    API_AUTH = (settings.MAUTIC_USER, settings.MAUTIC_PASS)

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
            # self.update_list("sustaining-list", (7,))
            # self.update_list("leadcontacts-list", contact_type=(6,))
            # self.update_list("allcontacts-list", contact_type=(4, 6, 9, 10, 11, 12, 13))

    def update_list(
        self,
        list_name="members-list",
        membership_status=(2, 3, 5, 7, 99),
        contact_type=(4, 6, 9, 10, 11, 12),
    ):
        offset = 0

        r = requests.get("{}/tags".format(self.API_URL), auth=self.API_AUTH)
        #
        resp = list(r.json()["tags"].values())
        tags = {}
        for item in resp:
            tags[item["tag"]] = item["id"]

        # emails = []
        # while True:
        #     r = requests.get("{}/contacts".format(self.API_URL), auth=self.API_AUTH)
        #     print(r.url)
        #     pprint(r.json())
        #
        #     break

        #
        for contact in Contact.objects.filter(
            contact_type__in=contact_type,
            organization__membership_status__in=membership_status,
            bouncing=False,
        )[:]:
            print(
                contact.first_name,
                contact.last_name,
                contact.email,
                contact.organization.associate_consortium,
            )

            consoritum = contact.organization.associate_consortium or ""
            if consoritum:
                consoritum = [consoritum.lower(), "members"]
            else:
                consoritum = ["members"]

            r = requests.post(
                "{}/contacts/new".format(self.API_URL),
                data={
                    "firstname": contact.first_name,
                    "lastname": contact.last_name,
                    "email": contact.email,
                    "tags": consoritum,
                },
                auth=self.API_AUTH,
            )
            print(r.json()["contact"]["id"])
