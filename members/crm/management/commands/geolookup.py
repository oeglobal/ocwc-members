# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from crm.models import Organization, Contact, Address

import geopy

class Command(BaseCommand):
	help = "Does a geolookup for Addresses that don't have it yet"
	args = ''

	def handle(self, *args, **options):
		for address in Address.objects.filter(city__isnull=False).exclude(latitude__isnull=False):
			print address.id, address.organization
			try:
				address.save()
			except:
				print 'no results'