import os

from django.conf import settings
from django.core.management.base import BaseCommand

import gspread


from conferences.models import (
    ConferenceEmailTemplate,
    ConferenceEmailRegistration,
    ConferenceEmailLogs,
)


class Command(BaseCommand):
    help = "Syncs google spreadsheet with db"

    def handle(self, *args, **options):
        gc = gspread.service_account(
            filename=os.path.join(settings.BASE_DIR, "members/service_account.json")
        )
        sh = gc.open_by_key(settings.CONFERENCE_SPREADSHEET_ID)
        worksheet = sh.get_worksheet(0)

        data = worksheet.get_all_records()

        for row in data:
            email = row["Email"]

            email_type = "normal"
            if row["Are you a presenter during the Conference?"] in ["Yes", "YES"]:
                email_type = "presenter"

            ConferenceEmailRegistration.objects.get_or_create(
                email=email, defaults={"email_type": email_type}
            )

        ConferenceEmailRegistration.objects.get_or_create(
            email="jure@oeglobal.org", email_type="presenter"
        )
        ConferenceEmailRegistration.objects.get_or_create(
            email="jure@oeconsortium.org", email_type="normal"
        )
