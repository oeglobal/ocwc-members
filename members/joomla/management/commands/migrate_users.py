# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from crm.models import Organization, Contact, Address

class Command(BaseCommand):
    help = "goes through Organizations and creates new users in Django system"

    def handle(self, *args, **options):
    	for org in Organization.objects.filter(membership_status__in=(2,3,5,7)):
    		# if org.contact_set.filter(contact_type=6).count():
    		# 	print org.get_absolute_staff_url()
    		lead_contact = org.contact_set.filter(contact_type=6).order_by('id')[0]
    		user, is_created = User.objects.get_or_create(
    			username = org.slug,
    			email = lead_contact.email
    		)
    		org.user = user
    		org.save()