# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from crm.models import Organization, Contact, Address

class Command(BaseCommand):
    help = "generates a list of emails with Lead Contact, Certifier and Voting representatives"

    def handle(self, *args, **options):
    	address_list = []

    	for contact in Contact.objects.filter(contact_type__in=(6,9,10), organization__membership_status__in=(2,3,5,7)):
    		if contact.email and contact.email not in address_list:
    			address_list.append(contact.email)

    	for email in address_list:
    		print "%s," % email