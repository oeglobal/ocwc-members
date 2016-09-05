from django.contrib import admin

from .models import ConferenceInterface, ConferenceRegistration

admin.site.register(ConferenceInterface)
admin.site.register(ConferenceRegistration)
