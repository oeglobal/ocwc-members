# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from crm.models import Organization, Contact, Address

class Command(BaseCommand):
    help = "removes duplicate contact information, that is left over from CiviCRM"

    def handle(self, *args, **options):
    	for org in Organization.objects.all():
    		print org.get_absolute_staff_url()
    		for lead_contact in org.contact_set.filter(contact_type=6):
	    		for contact in org.contact_set.all().exclude(pk=lead_contact.id):
	    			if contact.email == lead_contact.email:
	    				contact.delete()