from django.contrib import admin

from .models import (
    ConferenceInterface,
    ConferenceRegistration,
    ConferenceEmailTemplate,
    ConferenceEmailRegistration,
    ConferenceEmailLogs,
)


class ConferenceRegistrationAdmin(admin.ModelAdmin):
    list_display = ("interface", "name", "email", "organization", "payment_type")
    list_filter = ("interface", "payment_type")


@admin.register(ConferenceEmailTemplate)
class ConferenceEmailTemplate(admin.ModelAdmin):
    pass


@admin.register(ConferenceEmailRegistration)
class ConferenceRegistrationAdmin(admin.ModelAdmin):
    pass


@admin.register(ConferenceEmailLogs)
class ConferenceEmailLogs(admin.ModelAdmin):
    pass


admin.site.register(ConferenceInterface)
admin.site.register(ConferenceRegistration, ConferenceRegistrationAdmin)
