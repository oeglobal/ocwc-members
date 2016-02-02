# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from crm.models import Organization, Contact, Address

from optparse import make_option

class Command(BaseCommand):
	help = "Lists basic user information for input email addresses"
	args = '--emails'

	option_list = BaseCommand.option_list + (
		make_option("--emails", action="store", dest="emails", help="Comma separated list of emails"),
	)

	def handle(self, *args, **options):
		if options.get('emails'):
			emails = options.get('emails').split(',')
			for email in emails:
				print email, '\n'
				org = None
				for contact in Contact.objects.filter(email=email):


					if org != contact.organization.id:
						org = contact.organization.id
						print contact.organization.display_name
						print "http://members.oeconsortium.org/admin/crm/organization/%s/ \n" % contact.organization.id

						print contact.first_name, contact.last_name


					print contact.get_contact_type_display()

				print '---------\n\n'
