# -*- coding: utf-8 -*-
import csv

from django.core.management.base import BaseCommand

from joomla.models import CivicrmMembership, CivicrmValue1InstitutionInformation, CivicrmRelationship, JosUsers
from crm.models import Organization, Contact, Address

CiviInst = CivicrmValue1InstitutionInformation

class Command(BaseCommand):
    help = "migrates civicrm to new system"

    def handle(self, *args, **options):

        csv_file = csv.DictReader(open('sources/members.csv', 'rbU'), delimiter=',',quotechar='"')

        data = {}
        for line in csv_file:
            if line.get('CRM-ID'):
                data[line['CRM-ID']] = line

        for member in CivicrmMembership.objects.filter(
                membership_type__in=(5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17),
                status__in=[2,3,4,5,6,7]
            ):
            
            try:
                external_data = data[str(member.contact.id)]
            except KeyError:
                external_data = {}

            org, is_created = Organization.objects.get_or_create(
                
                display_name = member.contact.display_name,
                membership_type = member.membership_type.id,
                defaults = {
                    'legal_name': member.contact.legal_name or '',
                    'membership_status': member.status.id,
                    'crmid': member.contact.id,
                    'associate_consortium': external_data.get('AC -Member', '')
                }
            )

            if member.contact.civicrmaddress_set.exists():
                for civicrmaddress in member.contact.civicrmaddress_set.all():
                    if not civicrmaddress.street_address:
                        continue

                    if civicrmaddress.state_province:
                        state_province_name = civicrmaddress.state_province.name or ''
                        state_province_abbr = civicrmaddress.state_province.abbreviation or ''

                    if civicrmaddress.country:
                        country = civicrmaddress.country.name

                    address, is_created = Address.objects.get_or_create(
                        organization = org,
                        street_address = civicrmaddress.street_address,
                        defaults = {
                            'supplemental_address_1': civicrmaddress.supplemental_address_1 or '',
                            'supplemental_address_2': civicrmaddress.supplemental_address_2 or '',
                            'postal_code_suffix': civicrmaddress.postal_code_suffix or '',
                            'city': civicrmaddress.city or '',
                            'postal_code': civicrmaddress.postal_code or '',
                            
                            'state_province': state_province_name or '',
                            'state_province_abbr': state_province_abbr or '',                       

                            'country': country or '',
                            'latitude': civicrmaddress.geo_code_1,
                            'longitude': civicrmaddress.geo_code_2,
                        }
                    )

            try:
                institution = CivicrmValue1InstitutionInformation.objects.get(entity_id=member.contact.id)
                org.main_website = institution.main_website
                org.ocw_website = institution.ocw_website
                org.description = institution.description or ''
                org.logo_large = institution.seal_image__large
                org.logo_small = institution.seal_image__small
                org.rss_feed = institution.rss_course_feed
                org.accreditation_body = institution.accreditation_body_53 or ''
                org.support_commitment = institution.support_commitment_54 or ''

                org.save()
            except CivicrmValue1InstitutionInformation.DoesNotExist:
                pass
            
            contact_list = CivicrmRelationship.objects.filter(contact_id_b=member.contact.id)
            for civicontact_id in contact_list:
                civicontact = civicontact_id.contact_id_a

                try:
                    j = JosUsers.objects.get(id=civicontact.external_identifier)
                    email = j.email
                except (JosUsers.DoesNotExist, ValueError):
                    email = ''
                
                contact, is_created = Contact.objects.get_or_create(
                    organization = org,
                    contact_type = civicontact_id.relationship_type.id,
                    email = email,
                    first_name = civicontact.first_name or '',
                    last_name = civicontact.last_name or ''
                )
                