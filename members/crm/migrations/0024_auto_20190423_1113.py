# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-04-23 11:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("crm", "0023_auto_20190423_1110")]

    operations = [
        migrations.AlterField(
            model_name="billinglog",
            name="log_type",
            field=models.CharField(
                choices=[
                    (b"create_invoice", b"Invoice"),
                    (b"send_invoice", b"Send invoice via email"),
                    (b"create_paid_invoice", b"Create paid invoice"),
                    (b"send_paid_invoice", b"Send paid invoice via email"),
                    (b"create_note", b"Add a Billing note"),
                    (b"create_general_note", b"Add a General note"),
                    (b"create_payment", b"Payment"),
                ],
                max_length=30,
            ),
        )
    ]
