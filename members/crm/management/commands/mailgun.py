# -*- coding: utf-8 -*-
import requests
import json
from optparse import make_option

from django.core.management.base import BaseCommand
from django.conf import settings

from crm.models import Contact


class Command(BaseCommand):
    help = "tools to manage our mailgun email subscriptions"

    option_list = BaseCommand.option_list + (
        make_option("--get-bounces", action="store_true", dest="get_bounces", help="Downloads bounces and updates Contact record"),
        make_option("--update-list", action="store_true", dest="update_list", help="Updates members announce mailing list")
    )

    def handle(self, *args, **options):
        if options.get('get_bounces'):
            self.get_bounces()
        if options.get('update_list'):
            self.update_list()

    def get_bounces(self):
        r = requests.get('https://api.mailgun.net/v2/oeconsortium.org/bounces',
                auth=('api', settings.MAILGUN_APIKEY))
        data = json.loads(r.content)
        for bounce in data['items']:
            for contact in Contact.objects.filter(email__iexact=bounce.get('address'), bouncing=False):
                contact.bouncing = True
                contact.save()

                self.stdout.write(u"Marking {contact.email} as bouncing - {contact.first_name} {contact.last_name} from {contact.organization.display_name}".format(contact=contact))

    def update_list(self):
        offset = 0
        while True:
            r = requests.get("https://api.mailgun.net/v2/lists/members-list@oeconsortium.org/members",
                            auth=('api', settings.MAILGUN_APIKEY),
                            data={'skip': offset})

            data = json.loads(r.content)

            if not data['items']:
                break

            for mailing_member in data['items']:
                if Contact.objects.filter(email__iexact=mailing_member.get('address'), bouncing=True).exists():
                    r = requests.delete("https://api.mailgun.net/v2/lists/members-list@oeconsortium.org/members/" +
                                        mailing_member.get('address'),
                                        auth=('api', settings.MAILGUN_APIKEY))
                    d = json.loads(r.content)
                    print d.get('member').get('address'), d.get('message')

            offset += 100
