import xlwt
from django.core.management.base import BaseCommand

from elections.models import Election, CandidateBallot
from crm.models import Contact, Organization, LoginKey


class Command(BaseCommand):
    help = "exports Excel with members that didn't vote yet"

    def handle(self, *args, **options):
        self._members_list()

    def _members_list(self):
        orgs = []
        for org in Organization.objects.filter(membership_status__in=[2, 5, 7]):
            election = Election.objects.latest("id")

            if CandidateBallot.objects.filter(
                election=election, organization=org
            ).exists():
                continue

            orgs.append(org)

        wb = xlwt.Workbook(encoding="utf-8")
        ws = wb.add_sheet("Organizations")
        row_num = 0
        columns = [(u"ID", 25), (u"Name", 150), (u"Consortium", 150)]

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num][0], font_style)
            ws.col(col_num).width = columns[col_num][1] * 100

        font_style = xlwt.XFStyle()
        font_style.alignment.wrap = 1

        for obj in orgs:
            row_num += 1
            row = [obj.pk, obj.display_name, obj.associate_consortium or ""]

            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save("elections_didnt_vote.xls")
