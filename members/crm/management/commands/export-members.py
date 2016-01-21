# -*- coding: utf-8 -*-
from __future__ import print_function
from django.core.management.base import BaseCommand

from crm.models import Organization

class Command(BaseCommand):
    help = "exports active members and their contacts as XLS file"

    def handle(self, *args, **options):
        for org in Organization.active.all():
            # print org.display_name
            contact = org.contact_set.filter(contact_type=6).exclude(email='')
            if contact:
                contact = contact[0]
                application = org.membershipapplication_set.count()
                if application:
                    application_year = org.membershipapplication_set.latest('id').created.year
                else:
                    application_year = 'N/A'

                developing = org.address_set.latest('id').country.developing
                country = org.address_set.latest('id').country.name
                continent = org.address_set.latest('id').country.continent.name
                membership_type = org.get_membership_type_display()
                line = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (org.display_name, contact.first_name, contact.last_name, contact.email, application_year, developing, country, continent, membership_type)
                print(line.encode('utf-8'))
