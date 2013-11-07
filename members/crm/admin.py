from django.contrib import admin

from .models import Organization, Contact, Address, MembershipApplication, \
					MembershipApplicationComment, Country, ReportedStatistic

class OrganizationAdmin(admin.ModelAdmin):
	list_filter = ('membership_type', 'membership_status')
	list_display = ('display_name', 'associate_consortium', 'membership_status')
	search_fields = ('display_name',)

class AddressAdmin(admin.ModelAdmin):
	list_display = ('organization', 'street_address', 'city', 'country', 'latitude', 'longitude')

class ContactAdmin(admin.ModelAdmin):
	list_display = ('organization', 'contact_type', 'email', 'first_name', 'last_name')

class MembershipApplicationAdmin(admin.ModelAdmin):
	list_display = ('id', 'organization' , 'membership_type', 'legacy_application_id', 'main_website')
	list_filter = ('app_status',)

class MembershipApplicationCommentAdmin(admin.ModelAdmin):
	list_display = ('application', 'legacy_comment_id', 'legacy_app_id', 'comment', 'app_status')
	list_filter = ('app_status',)

class CountryAdmin(admin.ModelAdmin):
	list_display = ('name', 'iso_code', 'developing')
	list_filter = ('developing',)

class ReportedStatisticAdmin(admin.ModelAdmin):
	list_display = ('organization', 'last_modified', 'site_visits', 'orig_courses', 
					'trans_courses', 'orig_course_lang', 'trans_course_lang',
					'oer_resources', 'trans_oer_resources')
	search_fields = ('organization__display_name',)
	# list_filter = ('report_year',)

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(MembershipApplication, MembershipApplicationAdmin)
admin.site.register(MembershipApplicationComment, MembershipApplicationCommentAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(ReportedStatistic, ReportedStatisticAdmin)