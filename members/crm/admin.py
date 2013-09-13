from django.contrib import admin

from .models import Organization, Contact, Address

class OrganizationAdmin(admin.ModelAdmin):
	list_filter = ('membership_type', 'membership_status')
	list_display = ('display_name', 'associate_consortium', 'membership_status')

class AddressAdmin(admin.ModelAdmin):
	list_display = ('organization', 'street_address', 'city', 'country', 'latitude', 'longitude')

class ContactAdmin(admin.ModelAdmin):
	list_display = ('organization', 'contact_type', 'email', 'first_name', 'last_name')

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Address, AddressAdmin)