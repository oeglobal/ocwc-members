# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from joomla.models import OcwcStatistics
from crm.models import ReportedStatistic, Organization

class Command(BaseCommand):
    help = "migrates statistics to new system"

    def handle(self, *args, **options):
        self.stdout.write('Migrating statistics database')

        for civi_stat in OcwcStatistics.objects.all():
        	try:
        		org = Organization.objects.get(crmid=civi_stat.crm_org_id)
        	except Organization.DoesNotExist:
        		print "Missing:", civi_stat.crm_org_id
        		continue

        	statistic = ReportedStatistic.objects.create(
        		organization = org,
				report_month = civi_stat.report_month,
				report_year = civi_stat.report_year,
				site_visits = civi_stat.site_visits,
				orig_courses = civi_stat.orig_courses,
				trans_courses = civi_stat.trans_courses,
				orig_course_lang = civi_stat.orig_course_lang,
				trans_course_lang = civi_stat.trans_course_lang,
				report_date = civi_stat.report_date,
				last_modified = civi_stat.last_modified,
				carry_forward = civi_stat.carry_forward,

				oer_resources = civi_stat.oer_resources,
				trans_oer_resources = civi_stat.trans_oer_resources,
				comment = civi_stat.comment
        	)
        self.stdout.write("Completed Statistics migration")