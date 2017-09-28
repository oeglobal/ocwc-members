from django.contrib import admin

from .models import ConferenceInterface, ConferenceRegistration


class ConferenceRegistrationAdmin(admin.ModelAdmin):
    list_display = ('interface', 'name', 'email', 'organization', 'payment_type')
    list_filter = ('interface', 'payment_type')

admin.site.register(ConferenceInterface)
admin.site.register(ConferenceRegistration, ConferenceRegistrationAdmin)
