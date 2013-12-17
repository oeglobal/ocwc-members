# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from joomla.models import CivicrmValue1InstitutionInformation, CivicrmMembership, JosMemberApplications, CivicrmContact, CivicrmAddress
from crm.models import Organization, MembershipApplication, MembershipApplicationComment, Country

CiviInst = CivicrmValue1InstitutionInformation

class Command(BaseCommand):
	help = "updates import from CiviCRM"
	def handle(self, *args, **options):
		for org in Organization.objects.filter(crmid__isnull=False).exclude(crmid=''):
			crmid = org.crmid
			print org.id
			try:
				instinfo = CivicrmValue1InstitutionInformation.objects.get(entity_id=crmid)
			except CivicrmValue1InstitutionInformation.DoesNotExist:
				continue

			if not org.rss_course_feed and instinfo.rss_course_feed:
				org.rss_course_feed = instinfo.rss_course_feed
				org.save()
				print 'updated', org.display_name
