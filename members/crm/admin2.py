import djadmin2

from .models import Organization, Contact, Address

class OrganizationAdmin2(djadmin2.ModelAdmin2):
	list_filter = ('membership_type', 'membership_status')

djadmin2.default.register(Organization, OrganizationAdmin2)
djadmin2.default.register(Contact)
djadmin2.default.register(Address)