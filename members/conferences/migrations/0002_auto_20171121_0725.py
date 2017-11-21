# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('conferences', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conferenceregistration',
            name='billing_address',
            field=models.TextField(default=b'', blank=True),
        ),
        migrations.AlterField(
            model_name='conferenceregistration',
            name='billing_html',
            field=tinymce.models.HTMLField(default=b''),
        ),
        migrations.AlterField(
            model_name='conferenceregistration',
            name='conference_dinner',
            field=models.CharField(default=b'', max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='conferenceregistration',
            name='dinner_guest',
            field=models.CharField(default=b'', max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='conferenceregistration',
            name='reception_guest',
            field=models.CharField(default=b'', max_length=255, blank=True),
        ),
    ]
