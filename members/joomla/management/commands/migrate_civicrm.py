# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from joomla.models import *

CiviInst = CivicrmValue1InstitutionInformation

class Command(BaseCommand):
    help = "migrates civicrm to new system"

    def handle(self, *args, **options):
        for member in CivicrmMembership.objects.filter(
                membership_type__in=(5,10,11,12,9,17),
                status__in=[2,3,5,7]
            ):
            print member.contact.display_name, '\t',

            if member.contact.civicrmaddress_set.count():
                address = member.contact.civicrmaddress_set.all()[0]
                print address.country.name, '\t',
            else:
                print '\t',

            try:
                institution = CivicrmValue1InstitutionInformation.objects.get(entity_id=member.contact.id)
                print institution.main_website, '\t',
                print institution.ocw_website, '\t',
            except CivicrmValue1InstitutionInformation.DoesNotExist:
                print "\t",
            
            lead_contact_list = CivicrmRelationship.objects.filter(relationship_type=6, contact_id_b=member.contact.id)
            contacts = []
            for lead_contact_id in lead_contact_list:
                lead_contact = lead_contact_id.contact_id_a

                try:
                    j = JosUsers.objects.get(id=lead_contact.external_identifier)
                    name = "%s %s" % (lead_contact.display_name, lead_contact.display_name)
                    email = j.email

                    print name, "\t", email,
                    break
                except:
                    pass

            print ""
