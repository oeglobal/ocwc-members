# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from quickbooks.objects.invoice import Invoice as QuickBooksInvoice
from quickbooks.objects.payment import Payment as QuickBooksPayment
from quickbooks.exceptions import AuthorizationException
import arrow

from crm.models import Profile, Organization, Invoice, BillingLog
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Download information from QBO"

    def handle(self, *args, **options):
        self.get_qbo_events()

    def get_qbo_events(self):
        qb_client, profile = Profile.get_qb_client()

        user = User.objects.get(username="karen")

        for offset in [1, 100, 200, 300, 400, 500]:
            try:
                invoices = QuickBooksInvoice.all(qb=qb_client, start_position=offset)
            except AuthorizationException:
                profile.is_active = False
                profile.save()

                return

            for qb_invoice in invoices:
                try:
                    org = Organization.objects.get(qbo_id=qb_invoice.CustomerRef.value)
                except Organization.DoesNotExist:
                    continue

                log, is_created = BillingLog.objects.get_or_create(
                    qbo_id=qb_invoice.Id,
                    log_type="create_invoice",
                    defaults={
                        "organization": org,
                        "user": user,
                        "amount": qb_invoice.TotalAmt,
                    },
                )

                if is_created:
                    log.pub_date = arrow.get(
                        qb_invoice.MetaData["LastUpdatedTime"]
                    ).datetime
                    log.save()

        payments = QuickBooksPayment.all(qb=qb_client)
        for qb_payment in payments:
            try:
                org = Organization.objects.get(qbo_id=qb_payment.CustomerRef.value)
            except Organization.DoesNotExist:
                continue

            log, is_created = BillingLog.objects.get_or_create(
                qbo_id=qb_payment.Id,
                log_type="create_payment",
                defaults={
                    "organization": org,
                    "user": user,
                    "amount": qb_payment.TotalAmt,
                },
            )

            if is_created:
                log.pub_date = arrow.get(
                    qb_payment.MetaData["LastUpdatedTime"]
                ).datetime
                log.save()
