from django.db import models

ORGANIZATION_TYPE_CHOICES = (
	('university', 'Higher Education Institution'),
	('npo', 'Non-Profit Organization'),
	('ngo', 'Non-Governmental Organization'),
	('regionalconsortium', 'Regional Consortium'),
	('software', 'Software Development'),
	('commercial', 'Commercial Entity')
)

ORGANIZATION_MEMBERSHIP_TYPE_CHOICES = (
	('institution', 'Institutional Member'),
	('assoccons', 'Associate Consortium Member'),
	('affiliate', 'Organizational Member'),
	('corporate', 'Corporate Member')
)

class Organization(models.Model):
	legal_name = models.TextField()
	display_name = models.CharField()
	logo = models.ImageField(max_length=255)

	membership_type = models.CharField(max_length=255, choices=ORGANIZATION_MEMBERSHIP_TYPE_CHOICES)
	organization_type = models.CharField(max_length=255, choices=ORGANIZATION_TYPE_CHOICES)
	crmid = models.CharField(max_length=255, blank=True, help_text='Legacy identifier')

CONTACT_TYPE_CHOICES = (
	('lead', 'Main contact'),
	('tech', 'Technical contact'),
	('billing', 'Billing contact')
)

class Contact(models.Model):
	organization = models.ForeignKey(Organization)
	
	contact_type = models.CharField(max_length=25, choices=CONTACT_TYPE_CHOICES, default='lead')
	email = models.EmailField(max_length=255)

	first_name = models.CharField(max_length=255, blank=True, default='')
	last_name = models.CharField(max_length=255, blank=True, default='')

class Address(models.Model):
	organization = models.ForeignKey(Organization)

	street_address = models.CharField(max_length=255, blank=True, help_text='Street address with street number')
	city = models.CharField(max_length=255, blank=True)
	postal_code = models.CharField(max_length=50, blank=True)
	
	state_province = models.CharField(max_length=255)
	country = models.CharField(max_length=255, blank=True)

	latitude = models.FloatField(blank=True, null=True)
	longitude = models.FloatField(blank=True, null=True)
