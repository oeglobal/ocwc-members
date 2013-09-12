from django.db import models

ORGANIZATION_MEMBERSHIP_TYPE_CHOICES = (
	(5 , 'Institutional Members'),
	(6 , 'Organizational Members'),
	(7 , 'Associate Consortium Members'),
	(8 , 'Corporate Members - Basic'),
	(9 , 'Associate Institutional Members'),
	(10, 'Institutional Members - MRC'),
	(11, 'Institutional Members - DC'),
	(12, 'Institutional Members - DC - MRC'),
	(13, 'Organizational Members - DC'),
	(14, 'Associate Consortium Members - DC'),
	(15, 'Corporate Members - Premium'),
	(16, 'Corporate Members - Sustaining'),
	(17, 'Associate Institutional Members - DC')
)

ORGANIZATION_TYPE_CHOICES = (
	('university', 'Higher Education Institution'),
	('npo', 'Non-Profit Organization'),
	('ngo', 'Non-Governmental Organization'),
	('regionalconsortium', 'Regional Consortium'),
	('software', 'Software Development'),
	('commercial', 'Commercial Entity')
)

ORGANIZATION_MEMBERSHIP_STATUS = (
	(1,	'Applied'),
	(2,	'Current'),
	(3,	'Grace'),
	(4,	'Expired'),
	(5,	'Pending'),
	(6,	'Cancelled'),
	(7,	'Sustaining'),
	(8,	'Deceased'),
	(9,	'Testing'),
	(10,'Committee'),
	(11,'Committee'),
	(12,'Suspended'),
	(13,'New')
)

class Organization(models.Model):
	legal_name = models.CharField(max_length=255, blank=True)
	display_name = models.CharField(max_length=255)
	logo = models.ImageField(max_length=255, upload_to="logos")

	membership_type = models.IntegerField(max_length=10, choices=ORGANIZATION_MEMBERSHIP_TYPE_CHOICES)
	# organization_type = models.CharField(max_length=255, choices=ORGANIZATION_TYPE_CHOICES)
	membership_status = models.IntegerField(max_length=10, choices=ORGANIZATION_MEMBERSHIP_STATUS)
	crmid = models.CharField(max_length=255, blank=True, help_text='Legacy identifier')

	main_website = models.TextField(max_length=255, blank=True)
	ocw_website = models.TextField(max_length=255, blank=True)

	def __unicode__(self):
		return self.display_name

# CONTACT_TYPE_CHOICES = (
# 	('lead', 'Main contact'),
# 	('tech', 'Technical contact'),
# 	('billing', 'Billing contact')
# )

CONTACT_TYPE_CHOICES = (
	(6,	 'Lead Contact for'),
	(4,	 'Employee of'),
	(9,	 'Certifier for'),
	(10, 'Voting Representative'),
	(11, 'Affiliated with'),
	(12, 'AC Member of'),
)

class Contact(models.Model):
	organization = models.ForeignKey(Organization)
	
	contact_type = models.IntegerField(max_length=10, choices=CONTACT_TYPE_CHOICES)
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

