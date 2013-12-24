# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from joomla.models import CivicrmValue1InstitutionInformation, CivicrmMembership, JosMemberApplications, CivicrmContact, CivicrmAddress
from crm.models import Organization, MembershipApplication, MembershipApplicationComment, Country

CiviInst = CivicrmValue1InstitutionInformation

class Command(BaseCommand):
	help = "imports personal and contact information that first import missed"
	def handle(self, *args, **options):
		self.stdout.write('Updating Membership Applications')

		for app in MembershipApplication.objects.filter(legacy_application_id__isnull=False).exclude(app_status='Spam').filter(pk__in=(289,540)).order_by('id'):
			jos_app = JosMemberApplications.objects.get(pk=app.legacy_application_id)
			instinfo = CivicrmValue1InstitutionInformation.objects.get(entity_id=app.legacy_entity_id)

			try:
				jos_organization = jos_app.crm_contact_id_org
				# jos_individual = jos_app.crm_contact_id_ind
			except CivicrmContact.DoesNotExist:
				continue

			print '--------'
			# print jos_app
			print app.main_website, instinfo.main_website


			# print `jos_organization.display_name`
			
			print jos_organization.id
			# print jos_organization.first_name
			# print jos_organization.last_name

			#address
			# jos_address = CivicrmAddress.objects.get(contact=jos_individual)
			