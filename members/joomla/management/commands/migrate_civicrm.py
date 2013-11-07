# -*- coding: utf-8 -*-
import csv

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from joomla.models import CivicrmMembership, CivicrmValue1InstitutionInformation, CivicrmRelationship, JosUsers, CivicrmCountry, CivicrmAddress
from crm.models import Organization, Contact, Address, Country

def _civicrmaddress_to_address(civicrmaddress, org):
    if not (civicrmaddress.street_address or civicrmaddress.supplemental_address_1):
        return None

    if civicrmaddress.state_province:
        state_province_name = civicrmaddress.state_province.name or ''
        state_province_abbr = civicrmaddress.state_province.abbreviation or ''
    else:
        state_province_name = ''
        state_province_abbr = ''

    if civicrmaddress.country:
        # country = civicrmaddress.country.name
        country = Country.objects.get(name=civicrmaddress.country.name)
    else:
        country = None

    address, is_created = Address.objects.get_or_create(
        organization = org,
        street_address = civicrmaddress.street_address or '',
        defaults = {
            'supplemental_address_1': civicrmaddress.supplemental_address_1 or '',
            'supplemental_address_2': civicrmaddress.supplemental_address_2 or '',
            'postal_code_suffix': civicrmaddress.postal_code_suffix or '',
            'city': civicrmaddress.city or '',
            'postal_code': civicrmaddress.postal_code or '',
            
            'state_province': state_province_name,
            'state_province_abbr': state_province_abbr,

            'country': country,
            'latitude': civicrmaddress.geo_code_1,
            'longitude': civicrmaddress.geo_code_2,
        }
    )

    return address

class Command(BaseCommand):
    help = "migrates civicrm to new system"

    def handle(self, *args, **options):
        self.stdout.write('Migrating Country database')
        for civi_country in CivicrmCountry.objects.all():
            country = Country.objects.create(
                name = civi_country.name,
                iso_code = civi_country.iso_code,
                developing = civi_country.developing
            )

        for iso_code, name in [('AX', u'Åland Islands'), ('CI', u'Côte d’Ivoire')]:
            c = Country.objects.get(iso_code=iso_code)
            c.name = name
            c.save()

        del country

        self.stdout.write('Migrating CiviCRM database')
        csv_file = csv.DictReader(open('sources/members.csv', 'rbU'), delimiter=',',quotechar='"')

        data = {}
        for line in csv_file:
            if line.get('CRM-ID'):
                data[line['CRM-ID']] = line

        IL = User.objects.get(username='igorlesko')
        MM = User.objects.get(username='marcela')

        # for member in CivicrmMembership.objects.filter(pk=473):            
        for member in CivicrmMembership.objects.filter(
                membership_type__in=(5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17),
                status__in=[2,3,4,5,6,7]
            ):

            try:
                external_data = data[str(member.contact.id)]
            except KeyError:
                external_data = {}

            ocw_contact = None
            if external_data.get('MC') == 'IL':
                ocw_contact = IL
            elif external_data.get('MC') == 'MM':
                ocw_contact = MM

            org, is_created = Organization.objects.get_or_create(
                
                display_name = member.contact.display_name,
                membership_type = member.membership_type.id,
                defaults = {
                    'legal_name': member.contact.legal_name or '',
                    'membership_status': member.status.id,
                    'crmid': member.contact.id,
                    'associate_consortium': external_data.get('AC -Member', ''),
                    'ocw_contact': ocw_contact
                }
            )

            address = None
            for civicrmaddress in member.contact.civicrmaddress_set.all():
                address = _civicrmaddress_to_address(civicrmaddress, org)

            try:
                institution = CivicrmValue1InstitutionInformation.objects.select_related('institution_country').get(entity_id=member.contact.id)
                org.main_website = institution.main_website
                org.ocw_website = institution.ocw_website
                org.description = institution.description or ''
                if institution.seal_image__large:
                    org.logo_large = 'logos/'+institution.seal_image__large
                if institution.seal_image__small:
                    org.logo_small = 'logos/'+institution.seal_image__small
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

            #check if contact has address
            for civicrmaddress in civicontact.civicrmaddress_set.all():
                address = _civicrmaddress_to_address(civicrmaddress, org)

            if not org.address_set.all().exists() and institution.institution_country:
            # if not address and institution.institution_country:
                
                address, is_created = Address.objects.get_or_create(
                        organization = org,
                        street_address = '',
                        defaults = {
                            'country': Country.objects.get(iso_code=institution.institution_country.iso_code)
                        })


        self.stdout.write('Migration complete')