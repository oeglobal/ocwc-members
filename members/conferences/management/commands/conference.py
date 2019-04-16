# -*- coding: utf-8 -*-
from __future__ import print_function

import arrow

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from quickbooks.objects.detailline import SalesItemLine, SalesItemLineDetail
from quickbooks.objects.invoice import Invoice as QuickBooksInvoice
from quickbooks.objects.item import Item
from quickbooks.objects.term import Term
from quickbooks.objects.base import Ref, Address, EmailAddress, CustomerMemo
from quickbooks.exceptions import ValidationException
from quickbooks.objects.customer import Customer

from conferences.utils import sync_conference
from conferences.models import ConferenceRegistration, ConferenceInterface

from crm.models import Profile, Organization


class Command(BaseCommand):
    help = "synces conference information"

    def add_arguments(self, parser):
        parser.add_argument(
            "action", type=str, help="Actions: sync, send_invoice, gform-export"
        )
        parser.add_argument("--id", type=int, help="Conference Interface ID")

    def handle(self, *args, **options):
        if options.get("action") == "send_invoice":
            self._send_invoice(options.get("id"))

        if options.get("action") == "sync":
            conf_id = ConferenceInterface.objects.latest("id")
            sync_conference(conf_id.id)

        if options.get("action") == "gform-export":
            self._gform_export()

    def _send_invoice(self, _id):
        reg = ConferenceRegistration.objects.get(pk=_id)
        qb_client, profile = Profile.get_qb_client()

        invoice = QuickBooksInvoice()

        count = 1
        for product in reg.products:
            line = SalesItemLine()
            line.LineNum = count
            line.Amount = product["amount"] * product["price"]
            line.Description = product["name"]

            line.SalesItemLineDetail = SalesItemLineDetail()

            item = Item.get(settings.QB_CONFERENCE_ITEM_ID, qb=qb_client)
            line.SalesItemLineDetail.ItemRef = item.to_ref()
            line.SalesItemLineDetail.Qty = product["amount"]
            line.SalesItemLineDetail.UnitPrice = product["price"]
            line.SalesItemLineDetail.ServiceDate = arrow.now().format("YYYY-MM-DD")

            invoice.Line.append(line)

            count += 1

        customer = Customer.get(settings.QB_CONFERENCE_USER_ID, qb=qb_client)
        invoice.CustomerRef = customer.to_ref()

        term = Ref()
        term.value = 1
        invoice.SalesTermRef = term

        email = EmailAddress()
        email.Address = reg.email
        invoice.BillEmail = email

        address = Address()
        address.Line1 = reg.name
        address.Line2 = reg.billing_html
        invoice.BillAddr = address

        invoice.Deposit = None

        invoice.save(qb=qb_client)
        invoice_id = invoice.Id

        reg.qbo_id = invoice_id
        reg.save()

    def _gform_export(self):
        for org in Organization.active.all().exclude(membership_status=99):
            prefix = u"(s)" if org.membership_status == 7 else "(m)"
            print(u"{} | {} {}".format(org.display_name, prefix, org.display_name))
