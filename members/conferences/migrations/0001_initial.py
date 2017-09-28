# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConferenceInterface',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('url', models.CharField(default=b'', max_length=255)),
                ('api_key', models.CharField(default=b'', max_length=255)),
                ('private_key', models.CharField(default=b'', max_length=255)),
                ('last_synced', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ConferenceRegistration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('form_id', models.CharField(max_length=255)),
                ('entry_id', models.CharField(max_length=255)),
                ('entry_created', models.DateTimeField(null=True)),
                ('name', models.CharField(default=b'', max_length=255)),
                ('email', models.CharField(default=b'', max_length=255)),
                ('organization', models.CharField(default=b'', max_length=255)),
                ('billing_address', models.TextField(default=b'')),
                ('ticket_type', models.CharField(max_length=255)),
                ('dinner_guest', models.CharField(default=b'', max_length=255)),
                ('dinner_guest_qty', models.IntegerField(default=0)),
                ('conference_dinner', models.CharField(default=b'', max_length=255)),
                ('reception_guest', models.CharField(default=b'', max_length=255)),
                ('reception_guest_qty', models.IntegerField(default=0)),
                ('total_amount', models.CharField(max_length=255)),
                ('payment_type', models.CharField(max_length=255, choices=[(b'paypal', b'PayPal'), (b'wire', b'Wire Transfer')])),
                ('source_url', models.CharField(max_length=255)),
                ('billing_html', models.TextField(default=b'')),
                ('product_html', models.TextField(default=b'')),
                ('last_synced', models.DateTimeField(auto_now=True)),
                ('access_key', models.CharField(max_length=32, blank=True)),
                ('interface', models.ForeignKey(to='conferences.ConferenceInterface')),
            ],
        ),
    ]
